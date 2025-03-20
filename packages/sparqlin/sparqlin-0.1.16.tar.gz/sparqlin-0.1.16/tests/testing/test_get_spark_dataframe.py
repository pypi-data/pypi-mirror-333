import pytest
import yaml
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Import the function to be tested
from sparqlin.testing.helpers import create_spark_session, get_spark_dataframe


@pytest.fixture(scope="session")
def shared_tmp_path(tmp_path_factory):
    """
    Provides a module-scoped shared temporary directory.
    """
    return tmp_path_factory.mktemp("spark_test_shared")

@pytest.fixture(scope="session")
def custom_spark_session(shared_tmp_path, mock_yaml_file):
    """
    Module-scoped Pytest fixture generating Spark session using updated datasets_location parameter.
    """

    warehouse_location = shared_tmp_path / "spark-warehouse"
    warehouse_location.mkdir(parents=True, exist_ok=True)

    return create_spark_session(warehouse_location=warehouse_location.as_posix(),
                                datasets_location=mock_yaml_file.as_posix())

@pytest.fixture(scope="session")
def mock_yaml_file(shared_tmp_path):
    """
    Pytest fixture to create a mock YAML file for testing.
    """
    yaml_data = {
        "datasets": {
            "test_dataset": {
                "data": [
                    ["1", "Alice"],
                    ["2", "Bob"],
                    ["3", "Charlie"]
                ],
                "schema": [
                    {"name": "id", "type": "integer"},
                    {"name": "name", "type": "string"}
                ]
            }
        }
    }
    yaml_file = shared_tmp_path / "test_datasets.yaml"
    with open(yaml_file, "w") as f:
        yaml.dump(yaml_data, f)
    return yaml_file


def test_get_spark_dataframe_with_inline_data(custom_spark_session, mock_yaml_file):
    """
    Test the get_spark_dataframe function when the data is provided inline in the YAML file.
    """
    # Act
    df = get_spark_dataframe(custom_spark_session, mock_yaml_file.as_posix(), "test_dataset")

    # Assert
    expected_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    expected_data = [(1, "Alice"), (2, "Bob"), (3, "Charlie")]

    assert df.schema == expected_schema
    assert df.collect() == [pytest.approx(row) for row in expected_data]


def test_get_spark_dataframe_with_missing_dataset(custom_spark_session, mock_yaml_file):
    """
    Test the get_spark_dataframe function when the dataset is missing in the YAML file.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="Dataset 'non_existent_dataset' not found in the YAML configuration file."):
        get_spark_dataframe(custom_spark_session, mock_yaml_file.as_posix(), "non_existent_dataset")


def test_get_spark_dataframe_with_invalid_data_format(custom_spark_session, tmp_path):
    """
    Test the get_spark_dataframe function when the dataset data format is invalid.
    """
    # Create a YAML file with invalid data format
    yaml_data = {
        "datasets": {
            "test_dataset": {
                "data": {"invalid_field": "invalid_value"},  # This should not be a dictionary
                "schema": [
                    {"name": "id", "type": "integer"},
                    {"name": "name", "type": "string"}
                ]
            }
        }
    }
    yaml_file = tmp_path / "invalid_datasets.yaml"
    with open(yaml_file, "w") as f:
        yaml.dump(yaml_data, f)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid data format .* for dataset .*"):
        get_spark_dataframe(custom_spark_session, str(yaml_file), "test_dataset")