from __future__ import annotations

import configparser
import json
import logging
import time
import uuid
import queue
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from functools import partial, wraps
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
import requests
from tqdm import tqdm

from .df import (
    Df,
    df_type_conversions,
    response_single_datastream_to_df,
    series_to_patch_dict,
)
from .logging_constants import ISO_STR_FORMAT, TQDM_BAR_FORMAT, TQDM_DESC_FORMAT
from .sta import (
    Entities,
    Filter,
    FilterEntry,
    Order,
    OrderOption,
    Properties,
    Qactions,
    Settings,
    convert_to_datetime,
    log,
)

log = logging.getLogger(__name__)


def filter_cfg_to_query(filter_cfg: FilterEntry) -> str:
    filter_condition = ""
    if filter_cfg:
        range = filter_cfg.phenomenonTime.range
        format = filter_cfg.phenomenonTime.format

        t0, t1 = [datetime.strptime(str(ti), format) for ti in range]

        filter_condition = (
            f"{Properties.PHENOMENONTIME} gt {t0.strftime(ISO_STR_FORMAT)} and "
            f"{Properties.PHENOMENONTIME} lt {t1.strftime(ISO_STR_FORMAT)}"
        )
    log.debug(f"Configure filter: {filter_condition=}")
    return filter_condition


def retry(exception_to_check, tries=4, delay=3, backoff=2):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exception_to_check: the exception to check. may be a tuple of
        exceptions to check
    :type exception_to_check: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    """

    def deco_retry(f):  # pragma: no cover

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    logging.info(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


@retry(requests.HTTPError, tries=5, delay=1, backoff=2)
def get_with_retry(query: str):
    """
    This method retries to fetch data from the specified path according to the retry parameters
    :param path: the path which should be opened
    """
    auth = config.load_authentication()
    return requests.get(query, auth=auth)


@dataclass
class Entity:
    type: Entities
    id: int | None = None
    selection: List[Entities | Properties | None] = field(default_factory=list)
    settings: List[str | None] = field(default_factory=list)
    expand: List[Entity | Entities | None] = field(default_factory=list)
    filters: List[str | None] = field(default_factory=list)

    def __call__(self) -> str:
        out = f"{self.type}"
        if self.id:
            out += f"({self.id})"
        return out

    @property
    def filter(self) -> List[str | None]:
        return self.filters

    @filter.setter
    def filter(self, filter_i) -> None:
        self.filters += [filter_i]


class Query:
    def __init__(self, base_url: str, root_entity: Entities | Entity):
        self.base_url = base_url
        if isinstance(root_entity, Entities):
            self.root_entity = Entity(type=root_entity)
        else:
            self.root_entity = root_entity

    @staticmethod
    def selection_to_list(entity):
        out = []
        for si in entity.selection:
            out.append(si)
        return out

    @staticmethod
    def filter_to_str(entity):
        out = ""
        if entity:
            out = " and ".join(entity.filters)
        return out

    @staticmethod
    def settings_to_list(entity):
        out = []
        for si in entity.settings:
            out.append(si)
        return out

    @staticmethod
    def expand_to_list(entity):
        out = []
        if entity.expand:
            for ei in entity.expand:
                out_i = None
                if isinstance(ei, Entity):
                    out_i = ei.type(
                        [Filter.FILTER(Query.filter_to_str(ei))]
                        + Query.settings_to_list(ei)
                        + [Qactions.EXPAND(Query.expand_to_list(ei))]
                        + [Qactions.SELECT(Query.selection_to_list(ei))]
                    )
                else:
                    out_i = ei
                out.append(out_i)

        return list(out)

    def get_with_retry(self):
        """
        This method retries to fetch data from the specified path according to the retry parameters
        :param path: the path which should be opened
        """
        return get_with_retry(self.build())

    def build(self):
        out_list = [
            Filter.FILTER(Query.filter_to_str(self.root_entity)),
            Query.settings_to_list(self.root_entity),
            Qactions.SELECT(Query.selection_to_list(self.root_entity)),
            Qactions.EXPAND(Query.expand_to_list(self.root_entity)),
        ]
        out_list = list(filter(None, out_list))
        out = f"{self.base_url.strip('/')}/{self.root_entity()}"
        if out_list:
            out += "?"
            out += "&".join(out_list)

        return out


def build_query_datastreams(entity_id: int) -> str:
    obsprop = Entity(Entities.OBSERVEDPROPERTY)
    obsprop.selection = [Properties.NAME, Properties.IOT_ID]

    obs = Entity(Entities.OBSERVATIONS)
    obs.settings = [Settings.COUNT("true"), Settings.TOP(0)]
    obs.selection = [Properties.IOT_ID]

    ds = Entity(Entities.DATASTREAMS)
    ds.settings = [Settings.COUNT("true")]
    ds.expand = [obsprop, obs]
    ds.selection = [
        Properties.NAME,
        Properties.IOT_ID,
        Properties.DESCRIPTION,
        Properties.UNITOFMEASUREMENT,
        Entities.OBSERVEDPROPERTY,
    ]
    thing = Entity(Entities.THINGS)
    thing.id = entity_id
    thing.selection = [Properties.NAME, Properties.IOT_ID, Entities.DATASTREAMS]
    thing.expand = [ds]
    query = Query(base_url=config.load_sta_url(), root_entity=thing)
    query_http = query.build()

    return query_http


def get_request(query: Query | str) -> Tuple[int, dict]:
    if isinstance(query, Query):
        request = query.get_with_retry()
    else:
        request = get_with_retry(query)
    request_out = request.json()
    return request.status_code, request_out


def get_observations_count_thing_query(
    entity_id: int,
    filter_condition: str = "",
    filter_condition_datastreams: str = "",
    skip_n: int = 0,
) -> Query:
    observations = Entity(Entities.OBSERVATIONS)
    observations.settings = [Settings.COUNT("true")]
    observations.filter = filter_condition
    datastreams = Entity(Entities.DATASTREAMS)
    datastreams.settings = [Settings.SKIP(skip_n)]
    datastreams.filter = filter_condition_datastreams
    datastreams.selection = [Properties.OBSERVATIONS_COUNT]
    datastreams.expand = [observations]

    thing = Entity(Entities.THINGS)
    thing.id = entity_id
    thing.expand = [datastreams]
    thing.selection = [Entities.DATASTREAMS]
    query = Query(base_url=config.load_sta_url(), root_entity=thing)
    # query_http = query.build()

    return query


def get_results_n_datastreams_query(
    entity_id: int,
    n: int | None = None,
    skip: int | None = None,
    top_observations: int | None = None,
    filter_condition_observations: str = "",
    filter_condition_datastreams: str = "",
    expand_feature_of_interest: bool = True,
) -> Query:
    obs = Entity(Entities.OBSERVATIONS)
    obs.filter = filter_condition_observations
    obs.settings = [Settings.TOP(top_observations)]
    obs.selection = [
        Properties.IOT_ID,
        Properties.RESULT,
        Properties.PHENOMENONTIME,
        Properties.QC_FLAG,
    ]
    foi = Entity(Entities.FEATUREOFINTEREST)
    foi.selection = [Properties.COORDINATES, Properties.IOT_ID, Properties.FEATURE_FLAG]
    if expand_feature_of_interest:
        obs.expand = [foi]

    obsprop = Entity(Entities.OBSERVEDPROPERTY)
    obsprop.selection = [Properties.IOT_ID, Properties.NAME]

    ds = Entity(Entities.DATASTREAMS)
    ds.filter = filter_condition_datastreams
    ds.settings = [Settings.TOP(n), Settings.SKIP(skip)]
    ds.selection = [
        Properties.IOT_ID,
        Properties.UNITOFMEASUREMENT,
        Entities.OBSERVATIONS,
    ]
    ds.expand = [obs, obsprop]

    thing = Entity(Entities.THINGS)
    thing.id = entity_id
    thing.expand = [ds]
    thing.selection = [Entities.DATASTREAMS]
    query = Query(base_url=config.load_sta_url(), root_entity=thing)
    # query_http = query.build()

    return query


def get_results_n_datastreams(Q: Query | str):
    log.debug(f"Request {Q}")
    request = get_request(Q)
    # request = json.loads(Query(Entity.Thing).get_with_retry(complete_query).content)

    return request


def get_nb_datastreams_of_thing(thing_id: int) -> int:
    thing = Entity(Entities.THINGS)
    thing.id = thing_id
    ds = Entity(Entities.DATASTREAMS)
    ds.settings = [Settings.COUNT("true")]
    ds.selection = [Properties.IOT_ID]
    thing.expand = [ds]
    thing.selection = [Entities.DATASTREAMS]
    query = Query(base_url=config.load_sta_url(), root_entity=thing)
    query_http = query.build()

    nb_datastreams = (query.get_with_retry()).json().get("Datastreams@iot.count")

    return nb_datastreams


def response_datastreams_to_df(response: dict) -> pd.DataFrame:
    log.info("Building dataframe.")
    df_out = pd.DataFrame()
    for ds_i in response[Entities.DATASTREAMS]:
        nextLink = ds_i.get(f"{Entities.OBSERVATIONS}@iot.nextLink", None)
        if nextLink:
            log.warning("Not all observations are extracted!")  # TODO: follow link!
        # df_i = datastreams_response_to_df(ds_i)
        df_i = response_single_datastream_to_df(ds_i)
        df_out = df_type_conversions(pd.concat([df_out, df_i], ignore_index=True))
    log.info(f"Dataframe constructed with {df_out.shape[0]} rows.")
    return df_out


def get_total_observations_count(
    thing_id: int, filter_cfg: str, filter_cfg_datastreams: str
) -> int:
    total_observations_count = 0
    skip_streams = 0
    query_observations_count = get_observations_count_thing_query(
        entity_id=thing_id,
        filter_condition=filter_cfg,
        filter_condition_datastreams=filter_cfg_datastreams,
        skip_n=skip_streams,
    )
    log.info("Retrieving total number of observations.")
    bool_nextlink = True
    while bool_nextlink:
        _, response_observations_count = get_results_n_datastreams(
            query_observations_count
        )
        total_observations_count += sum(
            [
                ds_i["Observations@iot.count"]
                for ds_i in response_observations_count["Datastreams"]
            ]
        )
        skip_streams += len(response_observations_count["Datastreams"])
        query_observations_count = get_observations_count_thing_query(
            entity_id=thing_id,
            filter_condition=filter_cfg,
            filter_condition_datastreams=filter_cfg_datastreams,
            skip_n=skip_streams,
        )
        bool_nextlink = response_observations_count.get(
            "Datastreams@iot.nextLink", False
        )
        log.debug(f"temp count: {total_observations_count=}")
    log.info(
        f"Total number of observations to be retrieved: {total_observations_count}"
    )
    return total_observations_count


def update_response(
    d: dict[str, int | float | str | list], u: dict[str, str | list]
) -> dict[str, int | float | str | list]:
    common_keys = set(d.keys()).intersection(u.keys())

    assert all([type(d[k]) == type(u[k]) for k in common_keys])

    for k, v in u.items():
        if isinstance(v, list) and k in d.keys():
            d[k] = sum([d[k], v], [])
        else:
            d[k] = v
    return d


def get_query_response(
    query: Query, total_count: int | None = None, follow_obs_nextlinks: bool = True
) -> dict:
    status_code, response = 0, {}

    log.info("Execute query.")

    status_code, response_i = get_results_n_datastreams(query)
    response = update_response(response, response_i)
    # follow nextLinks (Datastreams)
    query = response_i.get(Entities.DATASTREAMS + "@iot.nextLink", None)
    while query:
        status_code, response_i = get_results_n_datastreams(query)
        if status_code != 200.0:
            raise RuntimeError(f"response with status code {status_code}.")
        # response[Entities.DATASTREAMS] = update_response(response.get(Entities.DATASTREAMS, []), response_i)
        response[Entities.DATASTREAMS] = (
            response.get(Entities.DATASTREAMS, []) + response_i["value"]
        )

        query = response_i.get("@iot.nextLink", None)
        response[Entities.DATASTREAMS + "@iot.nextLink"] = str(query)
    if total_count:
        pbar = tqdm(
            total=total_count,
            desc=TQDM_DESC_FORMAT.format("Observations count"),
            bar_format=TQDM_BAR_FORMAT,
        )
        pbar.monitor.name = "Observations count"
    count_observations = 0
    for ds_i in response.get(Entities.DATASTREAMS, {}):  # type: ignore
        query = ds_i.get(Entities.OBSERVATIONS + "@iot.nextLink", None)
        query = [None, query][follow_obs_nextlinks]
        while query:
            retrieved_nb_observations = count_observations + len(
                ds_i[Entities.OBSERVATIONS]
            )
            log.debug(f"Number of observations: {retrieved_nb_observations}")

            status_code, response_i = get_results_n_datastreams(query)

            ds_i[Entities.OBSERVATIONS] = (
                ds_i.get(Entities.OBSERVATIONS, []) + response_i["value"]
            )
            query = response_i.get("@iot.nextLink", None)
            query = [None, query][follow_obs_nextlinks]
            ds_i[Entities.OBSERVATIONS + "@iot.nextLink"] = query
        count_observations += len(ds_i[Entities.OBSERVATIONS])
        if total_count:
            pbar.update(len(ds_i[Entities.OBSERVATIONS]))
    if total_count:
        pbar.close()

    return response


def get_all_data(
    thing_id: int,
    filter_cfg: str,
    filter_cfg_datastreams: str = "",
    count_observations: bool = False,
    message_str: str = None,
    result_queue: queue.Queue = None,
):
    message_str = message_str or f"Retrieving data of Thing {thing_id}."
    log.info(message_str)
    log.info(f"---- filter: {filter_cfg}")
    log.debug(message_str + f"with filter {filter_cfg}")

    total_observations_count = None
    # get total count of observations to be retrieved
    if count_observations:
        total_observations_count = get_total_observations_count(
            thing_id=thing_id,
            filter_cfg=filter_cfg,
            filter_cfg_datastreams=filter_cfg_datastreams,
        )

    # get the actual data
    query = get_results_n_datastreams_query(
        entity_id=thing_id,
        filter_condition_observations=filter_cfg,
        filter_condition_datastreams=filter_cfg_datastreams,
    )

    # TODO: refactor:
    #       due to different response from query constructed as above and iot.nextLink, not possible in same loop
    #       should rewrite code to get consistent result?
    #       might not be possible as initial query return complete structure
    response = get_query_response(query, total_count=total_observations_count)

    df_out = response_datastreams_to_df(response)

    if df_out.isna().any().any():
        log.warning(f"The dataframe has NAN values.")
    if df_out.empty:
        log.warning(f"No data retrieved.")
        if result_queue:
            result_queue.put(df_out)
        return df_out
    log.info(
        f"Quality flag counts as downloaded: {df_out[Df.QC_FLAG].value_counts(dropna=False).to_json()}"
    )
    log.debug(f"Columns of constructed df: {df_out.columns}.")
    log.debug(f"Datastreams observation types: {df_out[Df.OBSERVATION_TYPE].unique()}")
    if result_queue:
        result_queue.put(df_out)
    return df_out


def get_datetime_latest_observation():
    obs = Entity(Entities.OBSERVATIONS)
    obs.settings = [
        Order.ORDERBY(Properties.PHENOMENONTIME, OrderOption.DESC),
        Settings.TOP(1),
    ]
    obs.selection = [Properties.PHENOMENONTIME]

    query = Query(base_url=config.load_sta_url(), root_entity=obs)
    request = query.get_with_retry().content
    # https://sensors.naturalsciences.be/sta/v1.1/OBSERVATIONS?$ORDERBY=phenomenonTime%20desc&$TOP=1&$SELECT=phenomenonTime
    latest_phenomenonTime = convert_to_datetime(
        json.loads(request)["value"][0].get(Properties.PHENOMENONTIME)
    )
    return latest_phenomenonTime


def json_generator(large_json):
    # Start the JSON object with the "requests" key
    yield '{"requests":['

    # Get the list of requests from the original large JSON object
    requests_list = large_json["requests"]

    # Loop through each request in the list
    for i, req in enumerate(requests_list):
        # Convert the individual request to JSON and yield it
        yield json.dumps(req)

        # Add a comma after each request except the last one
        if i < len(requests_list) - 1:
            yield ","

    # Close the JSON array and object
    yield "]}"


def create_patch_json(
    df: pd.DataFrame,
    columns: List[Df] = [Df.IOT_ID, Df.QC_FLAG],
    url_entity: Entities = Entities.OBSERVATIONS,
    json_body_template: str | None = None,
) -> str:
    if df.empty:
        log.warning("No ouliers are flagged (empty DataFrame).")
        return Counter([])
    df["patch_dict"] = df[columns].apply(
        partial(
            series_to_patch_dict,
            columns=columns,
            url_entity=url_entity,
            json_body_template=json_body_template,
        ),
        axis=1,
    )
    if df["patch_dict"].empty:
        log.warning("Nothing to patch.")
        return Counter([])

    final_json = {"requests": df["patch_dict"].to_list()}
    return final_json


def write_patch_to_file(
    final_json: str, file_path: Path, log_level: str = "INFO"
) -> None:
    json_filename = file_path.joinpath(uuid.uuid4().hex + ".json")

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    log.log(getattr(logging, log_level), f"json was written to file {json_filename}.")


def dry_run_skip(func):
    """Decorator to skip a function in dry-run mode."""

    def wrapper(*args, **kwargs):
        DRY_RUN = config.load_dryrun_var()
        if DRY_RUN:
            log.warning(f"[DRY-RUN] Skipping: {func.__name__}")
            return None  # Or some placeholder result if needed
        return func(*args, **kwargs)

    return wrapper


@dry_run_skip
def patch_qc_flags(
    df: pd.DataFrame,
    url: str,
    auth: Tuple[str, str] | None = None,
    columns: List[Df] = [Df.IOT_ID, Df.QC_FLAG],
    url_entity: Entities = Entities.OBSERVATIONS,
    json_body_template: str | None = None,
    bool_write_patch_to_file: bool = False,
) -> Counter:
    final_json = create_patch_json(
        df=df,
        columns=columns,
        url_entity=url_entity,
        json_body_template=json_body_template,
    )
    log.info(f"Start batch patch query {url_entity}.")

    try:
        response = requests.post(
            headers={"Content-Type": "application/json"},
            url=url,
            data=json_generator(final_json),
            auth=auth,
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        try:
            file_path = Path(log.root.handlers[1].baseFilename).parent  # type: ignore
        except:
            log.warning("Couldn't detect log location.")

        if not bool_write_patch_to_file:
            write_patch_to_file(
                final_json=final_json, file_path=file_path, log_level="WARNING"
            )
        # Handle HTTP errors
        if response.status_code == 502:
            log.error("Encountered a 502 Bad Gateway error.")
        elif response.status_code == 401:
            log.error("Incorrect authentication credentials.")
        else:
            log.error(f"An HTTP error occurred: {e}")

    except requests.exceptions.RequestException as e:
        # Handle other request-related exceptions
        log.error(f"An error occurred while making the request: {e}")

    except Exception as e:
        # Handle any other unexpected exceptions
        log.error(f"An unexpected error occurred: {e}")

    if response.status_code == 200:
        responses = response.json()["responses"]
        count_res = Counter([ri["status"] for ri in responses])
        log.info("End batch patch query")
        # log.info(f"{json.dumps(count_res)}")
        if set(count_res.keys()) != set(
            [
                200,
            ]
        ):
            log.error("Didn't succeed patching.")
    else:
        count_res = Counter([])

    return count_res


import io


def download_as_bytes_with_progress(url: str) -> bytes:
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    bio = io.BytesIO()
    with tqdm(
        desc=TQDM_DESC_FORMAT.format("File download"),
        bar_format=TQDM_BAR_FORMAT,
        total=total,
        unit="b",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in resp.iter_content(chunk_size=65536):
            bar.update(len(chunk))
            bio.write(chunk)
    return bio.getvalue()


def get_absolute_path_to_base():
    current_file = Path(__file__)
    idx_src = current_file.parts.index("src")
    out = current_file.parents[len(current_file.parts) - idx_src - 1]
    return out


def get_elev_netcdf(local_folder: Path | str = None) -> Path:
    url_ETOPO = "https://www.ngdc.noaa.gov/thredds/fileServer/global/ETOPO2022/60s/60s_bed_elev_netcdf/ETOPO_2022_v1_60s_N90W180_bed.nc"
    filename_ETOPO = url_ETOPO.rsplit("/", 1)[1]
    if local_folder is None:
        local_folder = get_absolute_path_to_base().joinpath("resources")
    local_file = (
        Path(local_folder).joinpath(filename_ETOPO)
    )

    if not local_file.exists():
        log.info("Downloading netCDF elevation file.")
        log.info(f"  file: {local_file}")
        r = requests.get(url_ETOPO, stream=True)
        with open(local_file, "wb") as f:
            f.write(download_as_bytes_with_progress(url_ETOPO))
        log.info("Download completed.")
    return local_file


def get_ne_10m_shp(local_folder: Path | str) -> None:
    urls = ["https://github.com/nvkelso/natural-earth-vector/raw/refs/heads/master/10m_physical/ne_10m_land.shp",
            "https://github.com/nvkelso/natural-earth-vector/raw/refs/heads/master/10m_physical/ne_10m_land.shx",
            "https://github.com/nvkelso/natural-earth-vector/raw/refs/heads/master/10m_physical/ne_10m_land.prj",
            "https://github.com/nvkelso/natural-earth-vector/raw/refs/heads/master/10m_physical/ne_10m_land.dbf",
            "https://github.com/nvkelso/natural-earth-vector/raw/refs/heads/master/10m_physical/ne_10m_land.cpg"]
    assert ~bool(local_folder.suffix), "The provided path is not a folder."
    Path(local_folder).mkdir(parents=True, exist_ok=True)
    for url in urls:
        filename = url.rsplit("/", 1)[1]
        local_file = Path(local_folder).joinpath(filename)

        if not local_file.exists():
            log.info("Downloading natural earth land polynomials.")
            log.info(f"  file: {local_file}")
            r = requests.get(url, stream=True)
            with open(local_file, "wb") as f:
                f.write(download_as_bytes_with_progress(url))
            log.info("Download completed.")


def set_sta_url(sta_url):
    if not isinstance(sta_url, str):
        logging.critical("The provided url (" + str(sta_url) + ") is not valid")
        return
    if not sta_url.endswith("/"):
        sta_url = sta_url + "/"
    config.set(STA_URL=sta_url)
    config.save()


def set_dryrun_var(dry_run: bool = False):
    config.set(DRY_RUN=["", True][dry_run])
    config.save()


FILENAME = ".staconf.ini"


class Config:
    """
    This class allows to store and load settings that are relevant for stapy
    Therefore one does not need to pass this arguments each time stapy is used
    """

    def __init__(self, filename=None):
        self.filename = filename
        if filename is None:
            self.filename = FILENAME
        self.config = configparser.ConfigParser()
        self.read()

    def read(self):
        self.config.read(self.filename)  # type: ignore

    def save(self):
        with open(self.filename, "w") as configfile:  # type: ignore
            self.config.write(configfile)

    def get(self, arg):
        try:
            return self.config["DEFAULT"][arg]
        except KeyError:
            return None

    def set(self, **kwargs):
        for k, v in kwargs.items():
            self.config["DEFAULT"][k] = str(v)

    def remove(self, arg):
        try:
            return self.config.remove_option("DEFAULT", arg)
        except configparser.NoSectionError:
            return False

    def load_sta_url(self):
        sta_url = self.get("STA_URL")
        if sta_url is None:
            log.critical(
                "The key (STA_URL) does not exist in the config file set the url first"
            )
            return ""
        return sta_url

    def load_dryrun_var(self):
        DRY_RUN = bool(self.get("DRY_RUN"))
        log.warning(f"{DRY_RUN=}")
        return DRY_RUN

    def load_authentication(self):
        sta_usr = self.get("STA_USR")
        sta_pwd = self.get("STA_PWD")
        if sta_usr is None or sta_pwd is None:
            log.debug("Sending the request without credentials")
            return None
        else:
            log.debug("Sending the request without credentials")
            return requests.auth.HTTPBasicAuth(sta_usr, sta_pwd)  # type: ignore


config = Config()
