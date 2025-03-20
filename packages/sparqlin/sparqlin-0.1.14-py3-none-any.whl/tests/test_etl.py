import pytest
from unittest.mock import MagicMock, patch
from pyspark.sql import DataFrame
from sparqlin.etl import ETL


@pytest.fixture
def mock_spark_session(mocker):
    """
    Fixture to mock the SparkSession and its methods.
    """
    mock_spark = mocker.MagicMock()
    mocker.patch("sparqlin.etl.SparkSession.builder.getOrCreate", return_value=mock_spark)
    return mock_spark


@pytest.fixture
def sample_dataframe():
    """
    Fixture to create a sample PySpark DataFrame mock for testing.
    """
    mock_dataframe = MagicMock(spec=DataFrame)
    return mock_dataframe


@pytest.fixture
def etl_instance(mock_spark_session):
    """
    Fixture to create an ETL instance with a mocked SparkSession.
    """
    return ETL(sql_query_path="fake_path.sql")


def test_extract_method_success(mocker, etl_instance):
    """
    Test the extract method to ensure it reads the SQL query correctly.
    """
    # Mock the open function to simulate reading from a file
    mock_query = "SELECT id, name FROM users;"
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_query))

    # Call the extract method
    sql_query = etl_instance.extract()

    # Assert that the output is as expected
    assert sql_query == mock_query


def test_extract_method_failure(mocker, etl_instance):
    """
    Test the extract method for failure scenario (e.g., file not found).
    """
    # Mock open to raise an exception
    mocker.patch("builtins.open", side_effect=FileNotFoundError("File not found"))

    # Assert that the method raises an exception
    with pytest.raises(FileNotFoundError):
        etl_instance.extract()


def test_transform_method_success(etl_instance, sample_dataframe):
    """
    Test the transform method to ensure SQL execution returns a DataFrame.
    """
    # Mock the Spark SQL method to return the mock DataFrame
    with patch.object(etl_instance.spark, "sql", return_value=sample_dataframe) as mock_sql:
        # SQL script to be executed
        sql_script = "SELECT id, name FROM users;"

        # Call the transform method
        result_dataframe = etl_instance.transform(sql_script)

        # Assert that the mock SQL method was called with the correct SQL script
        mock_sql.assert_called_once_with(sql_script)

        # Assert the result is the mocked DataFrame
        assert result_dataframe == sample_dataframe


def test_transform_method_failure(mock_spark_session, etl_instance):
    """
    Test the transform method for failure scenario (e.g., Spark SQL execution fails).
    """
    # Mock Spark SQL method to raise an exception
    mock_spark_session.sql.side_effect = Exception("SQL execution failed")

    # SQL script to be executed
    sql_script = "SELECT id, name FROM users;"

    # Assert that the method raises an exception
    with pytest.raises(Exception):
        etl_instance.transform(sql_script)


def test_load_method_success(sample_dataframe, mock_spark_session, etl_instance):
    """
    Test the load method to ensure DataFrame is written to a table successfully.
    """
    # Table name for testing
    table_name = "test_table"

    # Mock the write/saveAsTable operations
    sample_dataframe.write.mode.return_value.saveAsTable = MagicMock()

    # Call the load method
    etl_instance.load(sample_dataframe, table_name)

    # Assert the write.mode method was called with overwrite
    sample_dataframe.write.mode.assert_called_once_with("overwrite")

    # Assert the saveAsTable method was called
    sample_dataframe.write.mode.return_value.saveAsTable.assert_called_once_with(table_name)


def test_load_method_failure(mocker, sample_dataframe, etl_instance):
    """
    Test the load method for failure scenario (e.g., unable to write DataFrame).
    """
    # Table name
    table_name = "test_table"

    # Mock the saveAsTable method to raise an exception
    mocker.patch.object(
        sample_dataframe.write.mode.return_value,
        "saveAsTable",
        side_effect=Exception("Save to table failed"),
    )

    # Assert that the method raises an exception
    with pytest.raises(Exception):
        etl_instance.load(sample_dataframe, table_name)