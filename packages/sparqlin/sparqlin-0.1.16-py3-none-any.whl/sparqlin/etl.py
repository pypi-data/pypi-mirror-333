from pyspark.sql import SparkSession
from sparqlin.logging.logger_config import setup_logger  # Import the centralized logger setup


class ETL:
    """
    ETL class to handle Extract, Transform, and Load operations using the `sparqlin` framework.
    """

    def __init__(self, sql_query_path: str):
        """
        Initialize the ETL class with the SQL query file path.

        :param sql_query_path: Path to the Spark SQL query file.
        """
        self.sql_query_path = sql_query_path
        self.spark = SparkSession.builder.getOrCreate()  # Assumes SparkSession is preconfigured in Databricks
        self.logger = setup_logger(self.__class__.__name__)  # Use setup_logger for centralized logging

    def extract(self) -> str:
        """
        Extract the SQL query string from the provided file path.

        :return: SQL query as a string.
        """
        self.logger.info(f"Reading SQL query from file: {self.sql_query_path}")

        try:
            with open(self.sql_query_path, 'r') as sql_file:
                sql_script = sql_file.read()
            self.logger.info("SQL query successfully extracted.")
            return sql_script
        except Exception as e:
            self.logger.error(f"Failed to read the SQL query file: {self.sql_query_path}.", exc_info=e)
            raise

    def transform(self, sql_script: str):
        """
        Execute the provided SQL query and transform it into a DataFrame.

        :param sql_script: SQL query as a string.
        :return: A PySpark DataFrame produced by executing the SQL query.
        """
        self.logger.info("Executing SQL query using Spark session...")
        try:
            dataframe = self.spark.sql(sql_script)
            self.logger.info("SQL query executed successfully, resulting in a DataFrame.")
            return dataframe
        except Exception as e:
            self.logger.error("Failed to execute the SQL query.", exc_info=e)
            raise

    def load(self, dataframe, table_name: str):
        """
        Load the resulting DataFrame into a Databricks catalog as a table.

        :param dataframe: The DataFrame produced by the `transform` step.
        :param table_name: The name of the target table in the Databricks catalog.
        """
        self.logger.info(f"Saving DataFrame as a table: {table_name}")

        try:
            dataframe.write.mode("overwrite").saveAsTable(table_name)
            self.logger.info(f"DataFrame successfully saved to table: {table_name}")
        except Exception as e:
            self.logger.error(f"Failed to save the DataFrame as a table {table_name}.", exc_info=e)
            raise