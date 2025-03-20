import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, List, Tuple, Union

from dotenv import dotenv_values
from loguru import logger

from mepsy.env import (CONDA_PREFIX, GPU_DISCOVERY_SCRIPT, GPU_QUEUES,
                       MEPSY_SUBMITTED, PY4J, SPARK_HOME, SPARK_MAJOR_VERSION,
                       _check_spark_version, _spark_env_vars, _spark_submit)

MEP_MIN_MEMORY = 2
MEP_MAX_MEMORY = 48
SUPPORTED_CONFIG_KEYS = ("py_files", "environment",
                         "dotenvs", "files", "archives",
                         "kinit_env")


def argparse_parser(*args, **kwargs) -> argparse.ArgumentParser:
    """Return parser with default options:
    '-l'/'--local': used to test spark locally and trigger local vs cluster
    behaviors.

    '-o'/'--overwrite': used to overwrite elogs tables if used or can be used
    to customize script behavior with results, etc...

    Returns:
        argparse.ArgumentParser: parser object to be further customized if
        needed.
    """
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser.add_argument('-l', '--local', action='store_true')
    parser.add_argument('-o', '--overwrite', action='store_true')
    return parser


def kinit(kinit_env: Union[Path, str] = None):
    """Authenticate to Kerberos

    Args:
        kinit_env (Union[Path, str], optional): Path to .env file containing
        KINITPASS=xxxx credentials to authenticate to Kerberos.
        If not provided, it will look for KINITPASS value in the env vars
        and if also that is not present, it will skip the authentication.
        Defaults to None.
    """
    if kinit_env is not None:
        vals = dotenv_values(kinit_env)
        credentials = vals.get('KINITPASS')
    else:
        credentials = os.getenv('KINITPASS')

    if credentials is not None:
        subprocess.run(['kinit'], input=credentials, text=True)


def load_dotenvs(dotenvs=None):

    env_vars = {}

    dotenvs = [] if dotenvs is None else dotenvs

    for fn in dotenvs:
        env_vars.update(dotenv_values(fn))

    return env_vars


def spark_bool(val):
    if val:
        return "true"
    else:
        return "false"


def spark_context(local=False, threads='*', spark_version="3_2_0"):
    """
    Returns SparkContext for local run.
    if local is True, conf is ignored.

    Customized for VITO MEP
    """
    _check_spark_version(spark_version)
    spark_home = SPARK_HOME[spark_version]
    py4j_version = PY4J[spark_version]
    spark_major_version = SPARK_MAJOR_VERSION[spark_version]

    spark_py_path = [f'{spark_home}/python',
                     f'{spark_home}/python/lib/{py4j_version}-src.zip']

    env_vars = {'SPARK_MAJOR_VERSION': spark_major_version,
                'SPARK_HOME': spark_home}
    for k, v in env_vars.items():
        logger.info(f"Setting env var: {k}={v}")
        os.environ[k] = v

    logger.info(f"Prepending {spark_py_path} to PYTHONPATH")
    sys.path = spark_py_path + sys.path

    import py4j
    logger.info(f"py4j: {py4j.__file__}")

    import pyspark
    logger.info(f"pyspark: {pyspark.__file__}")

    import cloudpickle
    import pyspark.serializers
    from pyspark import SparkConf, SparkContext
    pyspark.serializers.cloudpickle = cloudpickle

    if local:
        logger.info(f"Setting env var: PYSPARK_PYTHON={sys.executable}")
        os.environ['PYSPARK_PYTHON'] = sys.executable

        conf = SparkConf()
        conf.setMaster(f'local[{threads}]')
        conf.set("spark.driver.bindAddress", "127.0.0.1")

        sc = SparkContext(conf=conf)
    else:
        sc = SparkContext()

    return sc


def _spark_parallelize(sc,
                       func,
                       iterable,
                       num_slices=None,
                       collect=True):
    """
    Run a spark for each safely with logging and exitlogs report if options
    are provided.
    """
    if num_slices is None:
        num_slices = len(iterable)

    if num_slices == 0:
        logger.warning("Nothing to process")
        return None

    try:

        logger.info(f"Starting parallelization of {len(iterable)} tasks.")

        if collect:
            rdd = sc.parallelize(iterable, num_slices).map(func).collect()
        else:
            rdd = sc.parallelize(iterable, num_slices).foreach(func)  # None

        logger.success("Spark processing completed.")

        return rdd

    except Exception as e:
        e_msg = str(e)
        if len(e_msg) > 4096:
            # when using telegram this causes an error because text is too long
            # so this prints the full error to the MEP logs
            print(e_msg)
            e_msg = e_msg[:4096]
        logger.error(f"ERROR - Task interrupted:\n{e}")
        # raise e # causes threadlock
        return e

    finally:

        sc.stop()


def spark_foreach(sc,
                  func,
                  iterable,
                  num_slices=None):
    return _spark_parallelize(sc,
                              func,
                              iterable,
                              num_slices=num_slices,
                              collect=False)


def spark_collect(sc,
                  func,
                  iterable,
                  num_slices=None):
    return _spark_parallelize(sc,
                              func,
                              iterable,
                              num_slices=num_slices,
                              collect=True)


class SparkApp:

    def __init__(self,
                 *,
                 config_path=None,
                 app_name="mepsy_app",
                 driver_memory=2,
                 executor_memory=2,
                 max_executors=1,
                 queue="default",
                 py_files=None,
                 environment=None,
                 archives=None,
                 files=None,
                 dotenvs=None,
                 env_vars=None,
                 wait_completion=False,
                 executor_cores=1,
                 memory_fraction=0.01,
                 shuffle_service=True,
                 dynamic_allocation=True,
                 max_result_size=0,
                 verbose=False,
                 local=False,
                 local_threads=1,
                 kinit_env=None,
                 include_gdal_vars=True,
                 spark_version="3_2_0",
                 extra_spark_options=None,
                 extra_spark_confs=None) -> None:

        self._local = local

        # memory is mainly allocated to memory overhead for the python app
        memory_overhead = self._memory_overhead(executor_memory)
        executor_memory = 1

        config = self._load_config(config_path)

        # attempt kerberos authentication
        kinit_env = (kinit_env if kinit_env is not None
                     else config.get("kinit_env"))
        kinit(kinit_env)

        py_files = self._update_args_from_config(
            py_files,
            config.get("py_files"))

        archives = self._update_kwargs_from_config(
            archives,
            config.get("archives"))

        files = self._update_args_from_config(
            files,
            config.get("files"))

        dotenvs = self._update_args_from_config(
            dotenvs,
            config.get("dotenvs"))
        env_vars = self._build_env_vars(spark_version=spark_version,
                                        env_vars=env_vars,
                                        dotenvs=dotenvs,
                                        include_gdal_vars=include_gdal_vars)
        if environment is None:
            environment = config.get("environment")
            if environment is None:
                raise ValueError("`environment` arg should be set, either "
                                 "in the args or config file.")

        spark_app_args = {
            "app_name": app_name,
            "driver_memory": driver_memory,
            "executor_memory": executor_memory,
            "memory_overhead": memory_overhead,
            "max_executors": max_executors,
            "queue": queue,
            "py_files": py_files,
            "archives": archives,
            "environment": environment,
            "files": files,
            "env_vars": env_vars,
            "wait_completion": wait_completion,
            "executor_cores": executor_cores,
            "memory_fraction": memory_fraction,
            "shuffle_service": shuffle_service,
            "dynamic_allocation": dynamic_allocation,
            "max_result_size": max_result_size
        }

        command = self._spark_submit_command(
            **spark_app_args,
            spark_version=spark_version,
            extra_spark_options=extra_spark_options,
            extra_spark_confs=extra_spark_confs)

        self._submit(
            command=command,
            env_vars=env_vars,
            verbose=verbose)

        # if script is local or already submitted, initialize context
        self.spark_context = spark_context(local=local,
                                           threads=local_threads,
                                           spark_version=spark_version)

    @staticmethod
    def _update_args_from_config(args, config_args):

        new_args = []
        if config_args:
            new_args += config_args

        if args:
            new_args += args

        if len(new_args) == 0:
            return None
        else:
            return new_args

    @staticmethod
    def _update_kwargs_from_config(kwargs, config_kwargs):

        new_kwargs = {}
        if config_kwargs:
            new_kwargs.update(config_kwargs)

        if kwargs:
            new_kwargs.update(kwargs)

        if len(new_kwargs) == 0:
            return None
        else:
            return new_kwargs

    @staticmethod
    def _load_config(config_path):

        if config_path is not None:
            with open(config_path, 'r') as f:
                mepsy_config = json.load(f)
        else:
            mepsy_config = {}

        for k in mepsy_config.keys():
            if k not in SUPPORTED_CONFIG_KEYS:
                raise ValueError(f"{k} key not in supported config keys "
                                 f"{SUPPORTED_CONFIG_KEYS}")
        return mepsy_config

    @staticmethod
    def _memory_overhead(executor_memory):

        if ((executor_memory < MEP_MIN_MEMORY) or
                (executor_memory > MEP_MAX_MEMORY)):
            raise ValueError(f"`executor_memory` needs to be between "
                             f" {MEP_MIN_MEMORY} and {MEP_MAX_MEMORY}")

        return executor_memory - 1

    def parallelize(self,
                    func: Callable,
                    iterable: Union[List, Tuple],
                    num_slices: int = None,
                    collect: bool = True):
        """shortcut method for: sc.parallelize(iterable, num_slices).map(func).collect()  # noqa: E501

        Args:
            func (Callable): Function to parallelize
            iterable (Union[List, Tuple]): arguments
            num_slices (int, optional): number of slices in which the tasks are
            parallelized. Defaults to len(iterable).
            collect (bool, optional): Collect rdd result. Defaults to True.

        Returns:
            _type_: RDD
        """
        return _spark_parallelize(self.spark_context,
                                  func,
                                  iterable,
                                  num_slices,
                                  collect)

    def foreach(self,
                func: Callable,
                iterable: Union[List, Tuple],
                num_slices: int = None):
        return _spark_parallelize(self.spark_context,
                                  func,
                                  iterable,
                                  num_slices,
                                  collect=False)

    @staticmethod
    def _is_running_on_cluster():
        submitted = os.getenv(MEPSY_SUBMITTED, "false").lower() == "true"
        return submitted

    @staticmethod
    def _build_env_vars(spark_version,
                        env_vars=None,
                        dotenvs=None,
                        include_gdal_vars=True):

        default_vars = _spark_env_vars(spark_version,
                                       include_gdal_vars)

        vars = load_dotenvs(dotenvs)
        vars[MEPSY_SUBMITTED] = "true"

        default_vars.update(vars)
        if env_vars is not None:
            default_vars.update(env_vars)

        return default_vars

    def _spark_submit_command(self,
                              *,
                              app_name,
                              driver_memory,
                              executor_memory,
                              memory_overhead,
                              max_executors,
                              queue="default",
                              py_files=None,
                              environment=None,
                              archives=None,
                              files=None,
                              env_vars=None,
                              wait_completion=True,
                              executor_cores=1,
                              memory_fraction=0.01,
                              shuffle_service=True,
                              dynamic_allocation=True,
                              max_result_size=0,
                              spark_version="3_2_0",
                              extra_spark_options=None,
                              extra_spark_confs=None):

        app_options = {
            "--name": app_name,
            "--driver-memory": f"{driver_memory}g",
            "--executor-memory": f"{executor_memory}g",
            "--queue": queue,
        }

        if extra_spark_options:
            app_options.update(extra_spark_options)

        if py_files:
            app_options.update({"--py-files": ",".join(py_files)})

        if files:
            app_options.update({"--files": ",".join(files)})

        if environment:
            app_options.update({"--archives": f"{environment}#{CONDA_PREFIX}"})

        if archives:
            arch_val = app_options.get("--archives")
            arch_extra_val = ",".join([f"{v}#{k}"
                                       for k, v in archives.items()])
            if arch_val is None:
                arch_val = arch_extra_val
            else:
                arch_val = f"{arch_val},{arch_extra_val}"

        app_confs = {
            "spark.executor.cores": executor_cores,
            "spark.task.cpus": executor_cores,
            "spark.executor.memoryOverhead": f"{memory_overhead}g",
            "spark.yarn.submit.waitAppCompletion": wait_completion,
            "spark.memory.fraction": memory_fraction,
            "spark.shuffle.service.enabled": spark_bool(shuffle_service),
            "spark.dynamicAllocation.enabled": spark_bool(dynamic_allocation),
            "spark.dynamicAllocation.maxExecutors": max_executors,
            "spark.driver.maxResultSize": max_result_size,
            "spark.ui.view.acls.groups": "vito"
        }

        if extra_spark_confs:
            app_confs.update(extra_spark_confs)

        command = [_spark_submit(spark_version),
                   '--master', 'yarn',
                   '--deploy-mode', 'cluster']

        for key, value in env_vars.items():
            app_confs[f'spark.yarn.appMasterEnv.{key}'] = value
            app_confs[f'spark.executorEnv.{key}'] = value

        for key, value in app_confs.items():
            command.append('--conf')
            command.append(f'{key}={value}')

        for key, value in app_options.items():
            command.extend([f'{key}', f'{value}'])

        # Get the path of the calling script
        caller_path = sys.modules['__main__'].__file__
        command.append(caller_path)

        args = sys.argv
        if len(args) > 1:
            command.extend(args[1:])

        return command

    def _submit(self, command, env_vars, verbose):

        # should not re-submit itself endlessly
        submitted = self._is_running_on_cluster()
        if submitted:
            return None

        local = self._local
        if verbose & local:
            logger.debug("*" * 10 + "spark-submit command" + "*" * 10)
            logger.debug("\n".join(command))
            print()

        if not local and not submitted:
            logger.debug("\n" + "*" * 10 + "Submitting to hadoop cluster" +
                         "*" * 10)
            print()

            if verbose:
                logger.debug("*" * 10 + "spark-submit command" + "*" * 10)
                logger.debug("\n".join(command))
                print()

            # overwrite SPARK env vars set by puppet which cause issues with SPARK 3  # noqa: E501
            os.environ.update(env_vars)

            # submit itself to cluster and exit the python script
            proc = subprocess.run(command, env=os.environ)
            sys.exit(proc.returncode)


class SparkGPUApp(SparkApp):

    def __init__(self,
                 *,
                 config_path=None,
                 app_name="mepsy_gpu_app",
                 driver_memory=30,
                 driver_cores=8,
                 queue="quadro",
                 py_files=None,
                 environment=None,
                 archives=None,
                 files=None,
                 dotenvs=None,
                 env_vars=None,
                 wait_completion=False,
                 memory_fraction=0.01,
                 verbose=False,
                 local=False,
                 kinit_env=None,
                 include_gdal_vars=True,
                 extra_spark_options=None,
                 extra_spark_confs=None) -> None:

        spark_version = "3_0_0"  # gpu cluster

        self._check_queue(queue)

        self._local = local

        # memory is mainly allocated to memory overhead for the python app
        memory_overhead = self._memory_overhead(driver_memory)
        driver_memory = 1

        config = self._load_config(config_path)

        # attempt kerberos authentication
        kinit_env = (kinit_env if kinit_env is not None
                     else config.get("kinit_env"))
        kinit(kinit_env)

        py_files = self._update_args_from_config(
            py_files,
            config.get("py_files"))

        archives = self._update_kwargs_from_config(
            archives,
            config.get("archives"))

        if files is None:
            files = []

        files.append(GPU_DISCOVERY_SCRIPT)
        files = self._update_args_from_config(
            files,
            config.get("files"))

        dotenvs = self._update_args_from_config(
            dotenvs,
            config.get("dotenvs"))
        env_vars = self._build_env_vars(spark_version=spark_version,
                                        env_vars=env_vars,
                                        dotenvs=dotenvs,
                                        include_gdal_vars=include_gdal_vars)
        if environment is None:
            environment = config.get("environment")
            if environment is None:
                raise ValueError("`environment` arg should be set, either "
                                 "in the args or config file.")

        spark_app_args = {
            "app_name": app_name,
            "driver_memory": driver_memory,
            "driver_memory_overhead": memory_overhead,
            "driver_cores": driver_cores,
            "queue": queue,
            "py_files": py_files,
            "archives": archives,
            "environment": environment,
            "files": files,
            "env_vars": env_vars,
            "wait_completion": wait_completion,
            "memory_fraction": memory_fraction
        }

        command = self._spark_submit_command(
            **spark_app_args,
            spark_version=spark_version,
            extra_spark_options=extra_spark_options,
            extra_spark_confs=extra_spark_confs)

        self._submit(
            command=command,
            env_vars=env_vars,
            verbose=verbose)

        self.spark_context = spark_context(local=local,
                                           threads=1,
                                           spark_version=spark_version)

    def _check_queue(self, queue):
        if queue not in GPU_QUEUES:
            raise ValueError(f"queue should be one of"
                             f" {self.supported_queues}")

    def _spark_submit_command(self,
                              *,
                              app_name,
                              driver_memory,
                              driver_memory_overhead,
                              driver_cores,
                              queue="quadro",
                              py_files=None,
                              environment=None,
                              archives=None,
                              files=None,
                              env_vars=None,
                              memory_fraction=0.01,
                              wait_completion=False,
                              gpu_amount=1,
                              spark_version="3_0_0",
                              extra_spark_options=None,
                              extra_spark_confs=None):

        app_options = {
            "--name": app_name,
            "--driver-memory": f"{driver_memory}g",
            "--queue": queue,
        }

        if extra_spark_options:
            app_options.update(extra_spark_options)

        if py_files:
            app_options.update({"--py-files": ",".join(py_files)})

        if files:
            app_options.update({"--files": ",".join(files)})

        if environment:
            app_options.update({"--archives": f"{environment}#{CONDA_PREFIX}"})

        if archives:
            arch_val = app_options.get("--archives")
            arch_extra_val = ",".join([f"{v}#{k}"
                                       for k, v in archives.items()])
            if arch_val is None:
                arch_val = arch_extra_val
            else:
                arch_val = f"{arch_val},{arch_extra_val}"

        app_confs = {
            "spark.driver.cores": driver_cores,
            "spark.driver.memoryOverhead": f"{driver_memory_overhead}g",
            "spark.driver.resource.gpu.amount": gpu_amount,
            "spark.driver.resource.gpu.discoveryScript": f"./{Path(GPU_DISCOVERY_SCRIPT).name}",  # noqa: E501
            "spark.yarn.submit.waitAppCompletion": wait_completion,
            "spark.memory.fraction": memory_fraction,
            "spark.ui.view.acls.groups": "vito"
        }

        if extra_spark_confs:
            app_confs.update(extra_spark_confs)

        command = [_spark_submit(spark_version),
                   '--master', 'yarn',
                   '--deploy-mode', 'cluster']

        for key, value in env_vars.items():
            app_confs[f'spark.yarn.appMasterEnv.{key}'] = value
            app_confs[f'spark.executorEnv.{key}'] = value

        for key, value in app_confs.items():
            command.append('--conf')
            command.append(f'{key}={value}')

        for key, value in app_options.items():
            command.extend([f'{key}', f'{value}'])

        # Get the path of the calling script
        caller_path = sys.modules['__main__'].__file__
        command.append(caller_path)

        args = sys.argv
        if len(args) > 1:
            command.extend(args[1:])

        return command
