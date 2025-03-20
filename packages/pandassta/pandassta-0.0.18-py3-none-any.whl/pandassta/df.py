import json
import logging
from copy import deepcopy
from functools import partial
from typing import List, Tuple
from pathlib import Path

import numpy as np
import pandas as pd
from geopandas import GeoDataFrame, points_from_xy
from geopy import distance as geopy_distance
from ordered_enum.ordered_enum import OrderedEnum
from pandas import DataFrame, Series
from pandas.api.types import CategoricalDtype
from strenum import StrEnum
from tqdm import tqdm

from .logging_constants import TQDM_BAR_FORMAT, TQDM_DESC_FORMAT
from .sta import Entities, Properties, convert_to_datetime

log = logging.getLogger(__name__)


class Df(StrEnum):
    IOT_ID = Properties.IOT_ID
    DATASTREAM_ID = "datastream_id"
    UNITS = "units"
    OBSERVATION_TYPE = "observation_type"
    QC_FLAG = Properties.QC_FLAG
    GRADIENT = "gradient"
    TIME = "phenomenonTime"
    RESULT = Properties.RESULT
    REGION = "Region"
    SUB_REGION = "Sub-region"
    LONG = "long"
    LAT = "lat"
    OBSERVED_PROPERTY_ID = "observed_property_id"
    FEATURE_ID = "feature_id"
    FEATURE_QC_FLAG= Properties.FEATURE_FLAG.replace("/", ".")
    DESCRIPTION = Properties.DESCRIPTION
    SENSOR = Entities.SENSOR
    ZSCORE = "zscore"


# not used, keep for future reference
# def features_request_to_df(request_features):
#     data = []
#     for fi in request_features["value"]:
#         v = fi.get(Properties.IOT_ID)
#         long, lat = fi.get("feature").get("coordinates")
#         idx = [oi.get(Properties.IOT_ID) for oi in fi.get(Entities.OBSERVATIONS)]
#         for idx_i in idx:
#             data.append([idx_i, v, long, lat])
#     df = pd.DataFrame(data, columns=[Df.IOT_ID, "feature_id", Df.LONG, Df.LAT])
#     return df


# not used
def response_obs_to_df(response_obs: dict) -> pd.DataFrame:
    # MISSING UNITS, TYPE, ...
    df = pd.DataFrame()
    df = pd.DataFrame(response_obs["value"]).astype(
        {Properties.IOT_ID: int, Df.RESULT: float}
    )
    df[Properties.PHENOMENONTIME] = df[Properties.PHENOMENONTIME].apply(
        convert_to_datetime
    )

    df[[Df.LONG, Df.LAT]] = pd.DataFrame.from_records(
        df[str(Entities.FEATUREOFINTEREST)].apply(
            lambda x: x.get("feature").get("coordinates")
        )
    )
    del df[str(Entities.FEATUREOFINTEREST)]

    return df


class QualityFlags(OrderedEnum):
    """
    http://vocab.nerc.ac.uk/collection/L20/current/

    Args:
        OrderedEnum (_type_): _description_

    Returns:
        _type_: _description_
    """

    NO_QUALITY_CONTROL = 0
    GOOD = 1
    PROBABLY_GOOD = 2
    PROBABLY_BAD = 3
    CHANGED = 5
    BELOW_detection = 6
    IN_EXCESS = 7
    INTERPOLATED = 8
    MISSING = 9
    PHENOMENON_UNCERTAIN = "A"
    NOMINAL = "B"
    BELOW_LIMIT_OF_QUANTIFICATION = "Q"
    BAD = 4

    def __str__(self):
        return f"{self.value}"


CAT_TYPE = CategoricalDtype(list(QualityFlags), ordered=True)


def process_feature_column(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df_features = pd.json_normalize(df.pop(str(Entities.FEATUREOFINTEREST))) # type: ignore
        try:
            df_features = df_features.rename( 
            columns={Df.IOT_ID: Df.FEATURE_ID},
            errors="raise"
        )
        except KeyError as e:
            df_features[Df.FEATURE_ID] = None

        df_coordinates = pd.DataFrame(
            df_features.pop("feature.coordinates").values.tolist(),
            columns=[Df.LONG, Df.LAT],
        )
        df_features = df_features.join(df_coordinates)
        df = df.join(df_features)

    except KeyError as e:
        df[[Df.FEATURE_ID, Df.LONG, Df.LAT]] = [None, None, None]

    return df


def response_single_datastream_to_df(response_datastream: dict) -> pd.DataFrame:
    df = pd.DataFrame()
    observations_list = response_datastream.get(Entities.OBSERVATIONS, [])
    log.debug(f"{observations_list=}")
    if observations_list:
        df_i = pd.DataFrame(observations_list).astype(
            {Properties.IOT_ID: int, Df.RESULT: float}
        )
        df_i[Df.QC_FLAG] = df_i.get(Df.QC_FLAG, QualityFlags.NO_QUALITY_CONTROL.value)  # type: ignore
        df_i[Df.QC_FLAG] = df_i[Df.QC_FLAG].fillna(0).astype(int).apply(QualityFlags).astype(CAT_TYPE)  # type: ignore
        df_i[Df.DATASTREAM_ID] = int(response_datastream.get(Properties.IOT_ID, -1))
        df_i[Properties.PHENOMENONTIME] = df_i[Properties.PHENOMENONTIME].apply(
            convert_to_datetime
        )
        if Properties.DESCRIPTION in response_datastream.keys():
            df_i[Properties.DESCRIPTION] = response_datastream.get(
                Properties.DESCRIPTION
            )
            df_i[Properties.DESCRIPTION] = df_i[Properties.DESCRIPTION].astype(
                "category"
            )
        if Entities.SENSOR in response_datastream.keys():
            df_i[str(Entities.SENSOR)] = response_datastream.get(
                Entities.SENSOR, {}
            ).get("name")
            df_i[str(Entities.SENSOR)] = df_i[str(Entities.SENSOR)].astype("category")
        df_i[Df.OBSERVATION_TYPE] = response_datastream.get(
            Entities.OBSERVEDPROPERTY, {}
        ).get(Properties.NAME)
        df_i[Df.OBSERVED_PROPERTY_ID] = response_datastream.get(
            Entities.OBSERVEDPROPERTY, {}
        ).get(Properties.IOT_ID)
        df_i[Df.OBSERVATION_TYPE] = df_i[Df.OBSERVATION_TYPE].astype("category")
        k1, k2 = Properties.UNITOFMEASUREMENT.split(
            "/", 1
        )  # could be improved by using df.join(pd.DataFrame(df.pop('COLUMNNAME').values.tolist()))
        df_i[Df.UNITS] = response_datastream.get(k1, {}).get(k2)
        df_i[Df.UNITS] = df_i[Df.UNITS].astype("category")

        df_i = process_feature_column(df_i)

        df = pd.concat([df, df_i], ignore_index=True)

    return df


# def response_datastreams_to_df(response: dict) -> pd.DataFrame:
#     df_out = pd.DataFrame()
#     for ds_i in response[Entities.DATASTREAMS]:
#         if f"{Entities.OBSERVATIONS}@iot.nextLink" in ds_i:
#             log.warning("Not all observations are extracted!")  # TODO: follow link!
#         df_i = response_single_datastream_to_df(ds_i)
#         log.debug(f"{df_i.shape[0]=}")
#         df_out = pd.concat([df_out, df_i], ignore_index=True)
#     return df_out


# def datastreams_response_to_df(response_datastreams):
#     df = pd.DataFrame()
#     for di in response_datastreams:
#         observations_list = di.get(Entities.OBSERVATIONS)
#         if observations_list:
#             df_i = pd.DataFrame(observations_list).astype(
#                 {Properties.IOT_ID: int, Df.RESULT: float}
#             )
#             df_i[Df.DATASTREAM_ID] = int(di.get(Properties.IOT_ID))
#             df_i[Properties.PHENOMENONTIME] = df_i[Properties.PHENOMENONTIME].apply(
#                 convert_to_datetime
#             )
#             df_i[Df.OBSERVATION_TYPE] = di.get(Entities.OBSERVEDPROPERTY).get(
#                 Properties.NAME
#             )
#             df_i[Df.OBSERVATION_TYPE] = df_i[Df.OBSERVATION_TYPE].astype("category")
#             k1, k2 = Properties.UNITOFMEASUREMENT.split("/", 1)
#             df_i[Df.UNITS] = di.get(k1).get(k2)
#             df_i[Df.UNITS] = df_i[Df.UNITS].astype("category")
#
#             df_i[[Df.LONG, Df.LAT]] = pd.DataFrame.from_records(
#                 df_i[str(Entities.FEATUREOFINTEREST)].apply(
#                     lambda x: x.get("feature").get("coordinates")
#                 )
#             )
#             del df_i[str(Entities.FEATUREOFINTEREST)]
#             # df_i.drop(columns=str(Entities.FEATUREOFINTEREST))
#             df = pd.concat([df, df_i], ignore_index=True)
#
#     return df


# def test_patch_single(id, value):
#     a = Patch.observation(entity_id=id, result_quality=str(value))
#     return a


def df_type_conversions(df):
    df_out = deepcopy(df)
    list_columns = [
        Df.OBSERVATION_TYPE,
        Df.UNITS,
        Df.REGION,
        Df.SUB_REGION,
        Properties.DESCRIPTION,
        Entities.SENSOR,
    ]
    for ci in set(list_columns).intersection(df.columns):
        mu0 = df_out[[ci]].memory_usage().get(ci)
        df_out[ci] = df_out[ci].astype("category")
        mu1 = df_out[[ci]].memory_usage().get(ci)
        if mu1 > mu0:
            log.warning("df type conversion might not reduce the memory usage!")

    if Df.QC_FLAG in df.columns:
        df_out[Df.QC_FLAG] = df_out[Df.QC_FLAG].astype(CAT_TYPE)
    for ci in set(list_columns).intersection(["bool"]):
        df_out[ci] = df_out[ci].astype("bool")

    return df_out


def series_to_patch_dict(
    x,
    group_per_x=1000,
    url_entity: Entities = Entities.OBSERVATIONS,
    columns: List[Df] = [Df.IOT_ID, Df.QC_FLAG],
    json_body_template: str | None = None,
):
    # qc_flag is hardcoded!
    # atomicityGroup seems to improve performance, but amount of groups seems irrelevant (?)
    # UNLESS multiple runs are done simultaneously?
    body_default = f'{{"{Properties.QC_FLAG}": "{{value}}"}}'
    if not json_body_template:
        json_body_template = body_default

    def create_json(template, value):
        # Load the JSON template
        template_json = json.loads(template)

        def replace_value(template_json, value):
            # Replace the placeholder with the given value
            for key, val in template_json.items():
                if isinstance(val, dict):
                    replace_value(val, value)
                elif isinstance(val, str) and "{value}" in val:
                    if isinstance(value, int):
                        template_json[key] = int(val.format(value=value))
                    elif isinstance(value, float):
                        template_json[key] = float(val.format(value))
                    else:
                        template_json[key] = val.format(value=value)

        replace_value(template_json, value)
        return template_json

    d_out = {
        "id": str(x.name + 1),
        "atomicityGroup": f"Group{(int(x.name/group_per_x)+1)}",
        "method": "patch",
        "url": f"{url_entity}({x.get(columns[0])})",
        "body": create_json(json_body_template, int(str(x.get(columns[1])))),
    }
    return d_out


def get_dt_series(df: DataFrame) -> Series:
    dt = (df[Df.TIME].shift(-1) - df[Df.TIME]).dt.total_seconds().abs()
    return dt


def get_distance_projection_series(df: DataFrame) -> Series:
    geodf = GeoDataFrame(  # type: ignore
        df.loc[:, [Df.TIME, Df.LAT, Df.LONG]],
        geometry=points_from_xy(df.loc[:, Df.LONG], df.loc[:, Df.LAT]),
    ).set_crs("EPSG:4326")
    distance = (
        geodf.to_crs("EPSG:4087").distance(geodf.to_crs("EPSG:4087").shift(-1)).abs()  # type: ignore
    )
    return distance


def get_distance_geopy_series(
    df: GeoDataFrame, column1: str = "geometry", column2: str = "None"
) -> Series:
    df_copy = deepcopy(df)

    def get_distance_geopy_i(row_i, column1=column1, column2=column2):
        point1 = row_i[column1]
        point2 = row_i[column2]
        if not point2:
            return None
        lat1: float = point1.y
        lon1: float = point1.x
        lat2: float = point2.y
        lon2: float = point2.x
        return geopy_distance.distance((lat1, lon1), (lat2, lon2)).meters

    if column2 == "None":
        column2 = "geometry_shifted"
        shifted_geometry_values = deepcopy(df["geometry"].shift(-1)).values  # type: ignore
        df_copy[column2] = shifted_geometry_values
    log.info("Start distance calculations.")
    tqdm.pandas(
        total=df.shape[0],
        bar_format=TQDM_BAR_FORMAT,
        desc=TQDM_DESC_FORMAT.format("Calculate distance"),
    )
    distances_series = df_copy.progress_apply(  # type: ignore
        partial(get_distance_geopy_i, column1=column1, column2=column2), axis=1
    )
    return distances_series  # type: ignore


def get_velocity_series(
    df: GeoDataFrame, return_dt=False
) -> Series | Tuple[Series, Series]:
    log.info("Velocity calculations.")
    # df_sorted = df.set_index(Df.FEATURE_ID).sort_values(Df.TIME)
    df_sorted = df.sort_values(Df.TIME).drop_duplicates(subset=[Df.TIME, Df.FEATURE_ID])
    dt = get_dt_series(df_sorted)
    distance = get_distance_geopy_series(df_sorted)  # type: ignore
    velocity = distance / dt

    velocity = velocity.bfill().replace(np.inf, np.nan)
    if return_dt:
        return (dt.rename("dt"), velocity.rename("velocity"))
    return velocity


def get_acceleration_series(
    df: GeoDataFrame, return_dt=False
) -> Series | Tuple[Series, Series]:
    log.info("Acceleration calculations.")
    df_sorted = df.sort_values(Df.TIME).drop_duplicates(subset=[Df.TIME, Df.FEATURE_ID])
    dt = get_dt_series(df_sorted)
    dt, velocity = get_velocity_series(df, return_dt=True)  # type: ignore

    accdt = velocity.shift(-1) - velocity
    acc = accdt / dt
    acc = acc.bfill().replace(np.inf, np.nan)
    if return_dt:
        return (dt.rename("dt"), acc.rename("acceleration))"))
    return acc.rename("acceleration))")


def get_dt_and_distance_series(df: GeoDataFrame) -> Tuple[Series, Series]:
    log.info("Distance calculations.")
    # df_tmp = df.sort_values(Df.TIME).groupby(Df.FEATURE_ID).first()
    df_tmp = df.sort_values(Df.TIME).drop_duplicates(subset=[Df.TIME, Df.FEATURE_ID])
    dt = get_dt_series(df_tmp)
    distance = get_distance_geopy_series(df_tmp)  # type: ignore
    return (dt, distance)


def get_dt_velocity_and_acceleration_series(
    df: GeoDataFrame,
) -> Tuple[Series, Series, Series]:
    log.info("Velocity and acceleration calculations.")
    dt, distance = get_dt_and_distance_series(df)

    velocity = distance / dt
    # velocity = (distance / dt).bfill()

    accdt = velocity.shift(-1) - velocity
    acc = accdt / dt

    velocity = velocity.bfill().replace(np.inf, np.nan)
    velocity = velocity.bfill().replace(-np.inf, np.nan)
    acc = acc.bfill().replace(np.inf, np.nan)
    acc = acc.bfill().replace(-np.inf, np.nan)
    velocity_out = Series(index=df.index)
    velocity_out.loc[velocity.index] = velocity
    velocity_out = velocity_out.rename("velocity")

    acc_out = Series(index=df.index)
    acc_out.loc[acc.index] = acc
    acc_out = acc_out.rename("acceleration")

    dt_out = Series(index=df.index)
    dt_out.loc[dt.index] = dt
    dt_out = dt_out.rename("dt")

    return (dt_out, velocity_out, acc_out)


def csv_to_df(input_file: Path | str) -> pd.DataFrame:
    df_out = pd.read_csv(input_file, index_col=0, parse_dates=[Df.TIME], date_format="mixed")

    

    for col in [Df.QC_FLAG, Df.OBSERVATION_TYPE, Df.UNITS]:
        df_out[col] = df_out[col].astype("category")

    df_out[Df.QC_FLAG] = df_out[Df.QC_FLAG].map(QualityFlags).astype(CAT_TYPE)
    if df_out.isnull().any().any():
        log.warning("The returned dataframe contains null values!")
    return df_out

# not in a test
# not used, keep for reference
# def do_qc(df: pd.DataFrame | gpd.GeoDataFrame, flag_config: QCFlagConfig) -> pd.Series:
#     bool_nan = flag_config.bool_function(df)
#     out = (
#         df[Df.QC_FLAG]
#         .combine(  # type: ignore
#             get_qc_flag_from_bool(
#                 bool_=bool_nan,
#                 flag_on_true=flag_config.flag_on_true,  # type: ignore
#             ),
#             flag_config.bool_merge_function,
#             fill_value=flag_config.flag_on_nan,  # type: ignore
#         )
#         .astype(CAT_TYPE)
#     )  # type: ignore
#     return out  # type: ignore
