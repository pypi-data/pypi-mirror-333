import os, sys
import shutil, re
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import yaml

import psutil
import git
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *


def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return Path(git_root).resolve()

def load_sql_scripts_from_path(directory: str) -> dict[str, str]:
    sql_dir = Path(get_git_root('.')) / directory
    if not sql_dir.exists():
        raise FileNotFoundError(f"Directory '{sql_dir}' not found.")

    scripts = {}
    # Load `.sql` files recursively
    for file_path in sql_dir.rglob("*.sql"):
        try:
            with file_path.open("r", encoding="utf-8") as f:
                scripts[file_path.name] = f.read()
        except (OSError, IOError) as e:
            print(f"Error reading file {file_path}: {e}")
    return scripts

def terminate_processes_using_directory(directory: str) -> None:
    for proc in psutil.process_iter(['pid', 'open_files']):
        for file in proc.info['open_files']:
            if file and file.path.startswith(directory):
                proc.kill()
                break

def terminate_java_processes() -> None:
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'java' in proc.info['name'].lower():
                proc.terminate()
                proc.wait()
                print(f"Terminated process {proc.info}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def find_process_using_file(file_path: str) -> psutil.Process:
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            open_files = proc.info.get('open_files', [])
            for file in open_files:
                if file and file.path == file_path:
                    return proc
        except psutil.AccessDenied:
            continue

def kill_process_using_file(file_path: str) -> None:
    proc = find_process_using_file(file_path)
    if proc:
        print(f"Killing process {proc.info['name']} with PID {proc.pid} ...")
        try:
            proc.kill()
            print(f"Killed process {proc.info['name']} with PID {proc.pid}")
        except psutil.Error as e:
            print(f"Error killing process {proc.info['name']} with PID {proc.pid}: {e}")
            print(f"Process {proc.info['pid']} already terminated.")
    else:
        print(f"No process using file {file_path} found.")

def clear_directory(directory: str) -> None:
    print(f"Clearing directory {directory} ...")
    terminate_java_processes()
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename != ".gitkeep":
                os.remove(os.path.join(root, filename))
            for dirname in dirs:
                dir_path = os.path.join(root, dirname)
                shutil.rmtree(dir_path)

def create_spark_session(warehouse_location: str, hive_location: str) -> SparkSession:
    app_name = "test"
    master = "local[2]"
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = (SparkSession
             .builder
             .appName(app_name)
             .master(master)
             .config("spark.sql.warehouse.dir", warehouse_location)
             .config("spark.driver.extraJavaOptions", f"-Dderby.system.home={Path(hive_location).as_posix()} -Dname=SparkTest")
             .enableHiveSupport()
             .getOrCreate())

    spark.sparkContext.setLogLevel("ERROR")
    print(f"Created Spark session with app name {app_name} and master {master}, "
          f"warehouse location at {spark.sparkContext.getConf().get('spark.sql.warehouse.dir')}.")

    return spark

def get_spark_dataframe(spark: SparkSession, yaml_file: str, dataset_name: str) -> DataFrame:
    """
    Reads a YAML configuration file, extracts a dataset by name, and creates a Spark DataFrame
    with appropriate data types based on schema.

    Args:
        spark: SparkSession object.
        yaml_file: Path to the YAML configuration file.
        dataset_name: Name of the dataset to read.

    Returns:
        DataFrame: Spark DataFrame with the specified dataset and schema applied.
    """

    # Map schema types to Spark SQL data types
    def map_spark_type(type_string):
        type_mapping = {
            "integer": IntegerType(),
            "long": LongType(),
            "string": StringType(),
            "float": FloatType(),
            "timestamp": TimestampType(),
            "boolean": BooleanType()
        }

        # Handle decimal type with precision and scale
        decimal_pattern = r"decimal\((\d+),\s*(\d+)\)" # Regex to match decimal(precision, scale)
        match = re.match(decimal_pattern, type_string.lower())
        if match:
            precision = int(match.group(1))
            scale = int(match.group(2))
            return DecimalType(precision, scale)

        # Default type mapping
        return type_mapping.get(type_string.lower(), StringType())

    # Convert string values to their appropriate data types
    def cast_value(value, spark_type):
        if value is None:
            return None
        if isinstance(value, str):
            if isinstance(spark_type, IntegerType) or isinstance(spark_type, LongType):
                return int(value)
            elif isinstance(spark_type, FloatType):
                return float(value)
            elif isinstance(spark_type, TimestampType):
                return datetime.fromisoformat(value)# or strptime(value, "%Y-%m-%d %H:%M:%S")
            elif isinstance(spark_type, DecimalType):
                precision = spark_type.precision
                scale = spark_type.scale
                return Decimal(str(value)).quantize(Decimal(f"1.{'0' * scale}"))
            elif isinstance(spark_type, BooleanType):
                return value.lower() in ("true", "1")
        return value

    # Load YAML configuration
    with open(yaml_file, "r") as f:
        config = yaml.safe_load(f)

    # Extract the dataset information
    dataset = config["datasets"].get(dataset_name)
    if not dataset:
        raise ValueError(f"Dataset '{dataset_name}' not found in the YAML configuration file.")

    data = dataset["data"]
    schema = dataset["schema"]

    # Build StructType schema by mapping schema definitions
    spark_schema = StructType([
        StructField(col["name"], map_spark_type(col["type"]), True) for col in schema
    ])

    # CASE 1: Data is given inline in the YAML (as rows)
    if isinstance(data, list):
        # Convert the raw data into rows with correct data types
        converted_data = [
            [cast_value(value, map_spark_type(col["type"])) for value, col in zip(row, schema)]
            for row in data
        ]
        # Return DataFrame using inline data
        return spark.createDataFrame(converted_data, schema=spark_schema)
    # CASE 2: Data is a path to a CSV file
    elif isinstance(data, str):
        # Load the CSV file using Spark
        data_csv_path = os.path.join(os.path.dirname(yaml_file), data)
        return spark.read.csv(data_csv_path, schema=spark_schema, header=True)

    else:
        raise ValueError(f"Invalid data format '{type(data)}' for dataset '{dataset_name}'.")

def register_all_tables(spark_session: SparkSession, datasets_file: str):
    """
    Registers all tables defined in the YAML configuration file as HIVE tables in Spark.

    :param spark_session: SparkSession object.
    :param datasets_file: Path to the YAML configuration file.
    :return:
    """
    with open(datasets_file, "r") as f:
        datasets = yaml.safe_load(f)

    # Assuming the YAML file defines the datasets in the form of a dictionary like:
    # datasets:
    # dataset_name_1: { data: [...], schema: [ {name: ..., type: ...} ]
    # dataset_name_2: { data: [...], schema: [ {name: ..., type: ...} ]
    for dataset_name, config in datasets["datasets"].items():
        # Split the dataset_name into parts
        parts = dataset_name.split('.')

        # Parse dataset_name
        if len(parts) == 3:  # Databricks Unity Catalog format
            catalog_name, schema_name, table_name = parts
            database_name = f"{catalog_name}_{schema_name}"  # Combine catalog and schema

        elif len(parts) == 2:  # Hive format
            database_name, table_name = parts

        else:
            raise ValueError(f"Invalid dataset_name format: {dataset_name}")

        # Create the database if it doesn't exist
        spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")

        # Get the Spark DataFrame for the dataset
        df = get_spark_dataframe(spark_session, datasets_file, dataset_name)

        # Save the DataFrame to the database.table name
        full_table_name = f"{database_name}.{table_name}"
        df.write.mode("overwrite").saveAsTable(full_table_name)
        print(f"Table registered: {full_table_name}")
