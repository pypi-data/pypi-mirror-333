import sys

MEPSY_SUBMITTED = 'MEPSY_SUBMITTED'

SUPPORTED_SPARK_VERSIONS = ["2_0_0", "3_0_0", "3_2_0"]

SPARK_HOME_2_0_0 = '/usr/hdp/current/spark2-client'
SPARK_HOME_3_0_0 = '/opt/spark3_0_0'
SPARK_HOME_3_2_0 = '/opt/spark3_2_0'

SPARK_HOME = {"2_0_0": SPARK_HOME_2_0_0,
              "3_0_0": SPARK_HOME_3_0_0,
              "3_2_0": SPARK_HOME_3_2_0}

PY4J = {"2_0_0": 'py4j-0.10.7',
        "3_0_0": 'py4j-0.10.8.1',
        "3_2_0": 'py4j-0.10.9.2'}

SPARK_MAJOR_VERSION = {"2_0_0": '2',
                       "3_0_0": '3',
                       "3_2_0": '3'}

GPU_DISCOVERY_SCRIPT = f"{SPARK_HOME_3_0_0}/bin/gpuDiscovery.sh"
GPU_QUEUES = ["quadro", "gtx1080ti"]

XDG_CACHE_HOME = ".cache"

CONDA_PREFIX = "./environment"

PYSPARK_PYTHON = f"{CONDA_PREFIX}/bin/python"

GDAL_ENV_VARS = dict(
    GDAL_CACHEMAX="128",
    GDAL_DATA=f"{CONDA_PREFIX}/share/gdal",
    GDAL_DRIVER_PATH=f"{CONDA_PREFIX}/lib/gdalplugins",
    CPL_ZIP_ENCODING="UTF-8",
    PROJ_LIB=f"{CONDA_PREFIX}/share/proj",
    PROJ_NETWORK="ON",
    GEOTIFF_CSV=f"{CONDA_PREFIX}/share/epsg_csv",
    GSETTINGS_SCHEMA_DIR=f"{CONDA_PREFIX}/share/glib-2.0/schemas")

PYTHON_BIN = {
    "PYSPARK_PYTHON": PYSPARK_PYTHON,
    "PYSPARK_DRIVER_PYTHON": PYSPARK_PYTHON,
}


class SparkVersionError(Exception):
    ...


def _check_spark_version(v):

    if v not in SUPPORTED_SPARK_VERSIONS:
        raise ValueError(f"spark_version: {v} is not among supported "
                         f"values {SUPPORTED_SPARK_VERSIONS}")

    # python < 3.8 is not supported by spark 3
    if ((sys.version_info.major < 4)
            and (sys.version_info.minor < 8)
            and (v != "2_0_0")):
        raise SparkVersionError("python < 3.8 is not supported by spark 3, "
                                "version should be '2_0_0'")


def _spark_env_vars(spark_version,
                    include_gdal_vars=True):
    _check_spark_version(spark_version)

    env_vars = dict(
        SPARK_HOME=SPARK_HOME[spark_version]
    )
    env_vars.update(PYTHON_BIN)

    if include_gdal_vars:
        env_vars.update(GDAL_ENV_VARS)

    return env_vars


def _spark_submit(spark_version):
    _check_spark_version(spark_version)
    return f"{SPARK_HOME[spark_version]}/bin/spark-submit"
