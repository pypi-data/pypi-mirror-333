import pytest
import yaml

from sparqlin.testing.helpers import get_spark_dataframe
from sparqlin.testing.base_test_config import BaseTestConfig
from sparqlin.testing.fixtures import spark_session, datasets_path, load_sql_scripts


@pytest.fixture(scope="module")
def hive_data_yaml(tmp_path_factory):
    """
    Creates a sample YAML configuration file with test tables and data.
    """
    tmp_path = tmp_path_factory.mktemp("datasets_test")
    datasets_content = {
        "datasets": {
            "testdb.test_table": {
                "data": [
                    ["1", "Alice"],
                    ["2", "Bob"],
                    ["3", "Charlie"]
                ],
                "schema": [
                    {"name": "id", "type": "integer"},
                    {"name": "name", "type": "string"}
                ]
            },
            "testdb.second_table": {
                "data": [
                    ["1", "100"],
                    ["2", "200"]
                ],
                "schema": [
                    {"name": "id", "type": "integer"},
                    {"name": "value", "type": "integer"}
                ]
            }
        }
    }

    datasets_file = tmp_path / "datasets.yml"
    with open(datasets_file, "w") as f:
        yaml.dump(datasets_content, f)

    return datasets_file, tmp_path

# Test case with dynamic datasets_path
@pytest.mark.parametrize("datasets_path",["tests/testing/datasets_test/datasets.yml"], indirect=True)
def test_base_test_config(spark_session, datasets_path):
    # Define the data
    test_table_df = get_spark_dataframe(spark_session, datasets_path, "testdb.test_table")
    second_table_df = get_spark_dataframe(spark_session, datasets_path, "testdb.second_table")
    assert test_table_df.count() == 3
    assert second_table_df.count() == 2

def test_load_sql_scripts(load_sql_scripts):
    sql_scripts = load_sql_scripts("tests/testing/sql")
    script1_query = sql_scripts["script1.sql"]
    script2_query = sql_scripts["script2.sql"]
    assert script1_query == "SELECT * FROM testdb.test_table;"
    assert script2_query == "SELECT * FROM testdb.second_table;"

def test_hive_table_operations(hive_data_yaml, tmp_path_factory):
    """
    Test persistent table creation, basic registration, and transformations.
    """
    datasets_file, tmp_path = hive_data_yaml

    # Step 1: Initialize BaseTestConfig using tmp_path_factory
    config = BaseTestConfig(tmp_path_factory)

    # Step 2: Update DATASETS_LOCATION to point to the existing datasets file
    config.DATASETS_LOCATION = datasets_file

    # Step 3: Create Spark session
    spark = config.create_spark_session()

    # Step 4: Register all tables using the YAML file
    config.register_tables(spark)

    # Verify table registration
    tables = spark.catalog.listTables("testdb")
    table_names = [table.name for table in tables]
    assert "test_table" in table_names
    assert "second_table" in table_names

    # Run transformations
    test_table_df = spark.sql("SELECT * FROM testdb.test_table")
    second_table_df = spark.sql("SELECT * FROM testdb.second_table")

    # Assert table content
    assert test_table_df.count() == 3
    assert test_table_df.filter(test_table_df.name == "Alice").count() == 1

    # Perform a join operation and verify results
    joined_df = test_table_df.join(second_table_df, test_table_df.id == second_table_df.id)
    joined_results = joined_df.select("name", "value").collect()

    assert len(joined_results) == 2
    assert any(row.name == "Alice" and row.value == 100 for row in joined_results)
    assert any(row.name == "Bob" and row.value == 200 for row in joined_results)