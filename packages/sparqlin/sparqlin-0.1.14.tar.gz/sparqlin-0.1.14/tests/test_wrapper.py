import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import col

pytestmark = pytest.mark.skip(reason="Disabling all tests in this file temporarily.")

# Fixture to create a SparkSession for the tests
@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder \
        .appName("test_suite") \
        .master("local[2]") \
        .getOrCreate()


# Helper function to create the `source_table` and `target_table`
def create_table(spark, table_name, data, schema):
    """Utility to create temporary Spark SQL tables for the tests."""
    df = spark.createDataFrame(data, schema)
    df.createOrReplaceTempView(table_name)


# Helper function to execute the query
def run_query(spark):
    """Executes the SQL query logic."""
    spark.sql("""
        WITH new_data AS (
            SELECT *
            FROM source_table
            WHERE date >= DATE_SUB(CURRENT_DATE(), 30)
              OR date > (SELECT MAX(date) FROM target_table)
        )
        INSERT INTO target_table
        SELECT * FROM new_data
    """)


# Helper function to check target table results
def get_target_table(spark):
    """Fetches data from the target table for validation."""
    return spark.sql("SELECT * FROM target_table")


# Start defining the test cases
def test_target_table_empty(spark):
    """Case 1: Target table is empty."""
    create_table(spark, "target_table", [], ["date", "id", "value"])
    create_table(spark, "source_table", [
        ("2023-10-01", 1, 100),
        ("2023-10-02", 2, 200)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # All rows from source_table should be inserted
    assert result_df.count() == 2


def test_source_table_empty(spark):
    """Case 2: Source table is empty."""
    create_table(spark, "target_table", [
        ("2023-10-01", 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # No changes should occur
    assert result_df.count() == 1


def test_both_tables_empty(spark):
    """Case 3: Both target and source tables are empty."""
    create_table(spark, "target_table", [], ["date", "id", "value"])
    create_table(spark, "source_table", [], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # Target table should remain empty
    assert result_df.count() == 0


def test_duplicate_dates_between_tables(spark):
    """Case 4: Duplicate dates exist between tables."""
    create_table(spark, "target_table", [
        ("2023-10-01", 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [
        ("2023-10-01", 1, 100),
        ("2023-10-02", 2, 200)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # Only the row with the new date should be inserted
    assert result_df.count() == 2
    assert result_df.filter(col("date") == "2023-10-02").count() == 1


def test_unordered_dates_in_source(spark):
    """Case 5: Source table contains unordered dates."""
    create_table(spark, "target_table", [
        ("2023-10-01", 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [
        ("2023-09-25", 2, 200),
        ("2023-10-03", 3, 300),
        ("2023-09-15", 4, 400)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # Only rows within the last 30 days or after 2023-10-01 should be included
    assert result_df.count() == 3


def test_no_overlap_between_tables(spark):
    """Case 6: No overlap between source and target dates."""
    create_table(spark, "target_table", [
        ("2023-10-01", 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [
        ("2023-10-02", 2, 200),
        ("2023-10-03", 3, 300)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # All rows from the source_table should be added
    assert result_df.count() == 3


def test_overlap_last_30_days(spark):
    """Case 7: Overlap in the last 30 days is reprocessed."""
    create_table(spark, "target_table", [
        ("2023-09-25", 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [
        ("2023-09-25", 1, 200),  # Overlapping date with new value
        ("2023-10-01", 2, 300)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # Overlapping rows should overwrite previous entries
    assert result_df.count() == 2
    assert result_df.filter(col("date") == "2023-09-25").first()["value"] == 200


def test_null_dates_in_tables(spark):
    """Case 8: Null values in the date column."""
    create_table(spark, "target_table", [
        (None, 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [
        (None, 2, 200),
        ("2023-10-02", 3, 300)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # Rows with null dates should not affect the logic
    assert result_df.count() == 2
    assert result_df.filter(col("id") == 3).count() == 1


def test_future_dates_in_source(spark):
    """Case 9: Source table contains future dates."""
    create_table(spark, "target_table", [
        ("2023-10-01", 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [
        ("2023-11-01", 2, 200)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # Future-dated rows should be inserted
    assert result_df.count() == 2
    assert result_df.filter(col("date") == "2023-11-01").count() == 1


def test_partial_target_table_inconsistencies(spark):
    """Case 10: Target table contains partially missing data."""
    create_table(spark, "target_table", [
        ("2023-09-25", 1, 100)
    ], ["date", "id", "value"])
    create_table(spark, "source_table", [
        ("2023-09-25", 1, 150),  # Updated row
        ("2023-10-02", 2, 200)
    ], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # Updated rows should be inserted
    assert result_df.count() == 2
    assert result_df.filter(col("id") == 1).first()["value"] == 150


def test_large_source_table(spark):
    """Case 11: Very large source table."""
    large_data = [(f"2023-10-{str(i).zfill(2)}", i, i * 100) for i in range(1, 101)]
    create_table(spark, "source_table", large_data, ["date", "id", "value"])
    create_table(spark, "target_table", [], ["date", "id", "value"])

    run_query(spark)
    result_df = get_target_table(spark)

    # All 100 rows should be inserted
    assert result_df.count() == 100