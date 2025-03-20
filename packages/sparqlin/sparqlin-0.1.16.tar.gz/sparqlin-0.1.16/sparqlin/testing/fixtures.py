# testing/fixtures.py
import os

import pytest
import time
from pyspark.sql.types import TimestampType

from sparqlin.testing.helpers import get_git_root, load_sql_scripts_from_path
from sparqlin.testing.base_test_config import BaseTestConfig

@pytest.fixture(scope="module")
def load_sql_scripts():
    """
    Fixture to load all SQL scripts from a specified directory.
    """
    return load_sql_scripts_from_path

@pytest.fixture(scope="module")
def datasets_path(request):
    """
    Fixture to generate a dataset path dynamically based on the parameter.
    """
    # Return an absolute path to the datasets file
    return str(get_git_root('.') / getattr(request, "param", None))

@pytest.fixture(scope="module")
def spark_session(tmp_path_factory, datasets_path):
    """
    Centralized spark_session fixture for creating and managing Spark sessions.
    Uses the BaseTestConfig class for configuration.
    """
    print(f"datasets_location: {datasets_path}")
    if datasets_path is None:
        print("No datasets location provided, using default.")

    # Create a default configuration object (can be subclassed if needed)
    config = BaseTestConfig(tmp_path_factory, datasets_path)

    # Create SparkSession
    spark = config.create_spark_session()

    # Register the mock `now()` function
    spark.udf.register("now", lambda: config.mock_now, TimestampType())

    # Register all tables from the dataset
    config.register_tables(spark)

    # Yield SparkSession to tests
    yield spark

    # Teardown logic stop SparkSession and clean directories
    spark.stop()
    time.sleep(3)  # Allow Spark to fully release file locks