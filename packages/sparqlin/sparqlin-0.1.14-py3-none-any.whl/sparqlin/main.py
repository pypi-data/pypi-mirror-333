import argparse

from sparqlin.etl import ETL  # Import the ETL class
from sparqlin.logging.logger_config import setup_logger  # Import the centralized logger setup


def main():
    """
    Orchestrates the ETL process for a given SQL query.
    """
    logger = setup_logger("ETL_Main")  # Get a logger for the main script

    # Command-line arguments for defining SQL and table parameters
    parser = argparse.ArgumentParser(description="Run the ETL process for a given SQL query in Databricks.")
    parser.add_argument(
        "--sql-query-path",
        required=True,
        help="Path to the SQL query file to be executed."
    )
    parser.add_argument(
        "--table-name",
        required=True,
        help="Target Databricks table name to save the resulting DataFrame."
    )

    args = parser.parse_args()
    sql_query_path=args.sql_query_path
    table_name=args.table_name

    logger.info("Starting the ETL process...")

    # Instantiate the ETL class
    etl = ETL(sql_query_path=sql_query_path)

    try:
        # Step 1: Extract
        sql_script = etl.extract()

        # Step 2: Transform
        dataframe = etl.transform(sql_script=sql_script)

        # Step 3: Load
        etl.load(dataframe=dataframe, table_name=table_name)

        logger.info("ETL process completed successfully.")
    except Exception as e:
        logger.error("ETL process failed.", exc_info=e)
        raise


if __name__ == "__main__":
    main()