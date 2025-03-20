# sparqlin

`sparqlin` is a **Spark SQL framework** designed to simplify job creation and management in **Databricks** environments. 
It integrates with Spark SQL and PySpark for a streamlined development experience.

The framework was specifically created to empower **data analysts** who may not have deep development skills. 
It provides a streamlined approach to adopting standard software development life cycles, 
enabling analysts to focus on working with data without the need to master complex programming paradigms. 
By leveraging familiar tools like SQL scripts and YAML files, the framework simplifies tasks such as data configuration, transformation, and testing.

This enables teams to:
- Bridge the gap between data analysis and software engineering.
- Enhance collaboration and maintain clear development processes.
- Encourage reusable and maintainable data workflows, all while adhering to best practices.

## Features
- Simplifies the creation of Spark SQL jobs for Databricks.
- Flexible integration with PySpark and Spark SQL.
- YAML-based configuration for job definitions.
- Built-in support for testing through `pytest`.
- Integrated with tools like `GitPython` and system monitoring via `psutil`.
- Works with Databricks Bundles.

## Installation
You can install `sparqlin` directly from PyPI using `pip`.
```pip install sparqlin```

### Requirements
`sparqlin` requires Python 3.11 or higher (Databricks Runtime 15.4 LTS). Ensure you have the following dependencies installed:
- `pyspark>=3.5.0`
- `pytest`
- `pyyaml`
- `psutil`
- `gitpython`

## Getting Started
### Example Usage of ETL framework
To use `sparqlin` for creating and running Spark SQL jobs in Databricks, follow these steps:
1. **Initialize a Project**: Start by creating a structure for your project. For instance, define YAML configuration files 
   for your Databricks jobs.
2. **Create Spark SQL transformations**: You can create a directory and place .sql files with queries that will run on Databricks.
3. **Load and Run Jobs**: Use the provided framework functionality to parse configurations and execute jobs efficiently in Databricks.

Here is a typical layout of an analytical project:
```text
databricks_default_project/
|-- README.md
|-- sql/
|   |-- query1.sql
|   |-- query2.sql
|   |-- ...
|-- tests/
|   |-- __init__.py
|   |-- test_query1.py
|   |-- test_query2.py
|   |-- ...
|-- databricks.yml
```

Below is an example configuration of jobs and tasks **databricks_default_project.job.yml**:

```yaml
# The example job configuration for databricks_default_project.
resources:
  jobs:
    databricks_default_python_job:
      trigger:
        # Run this job every day, exactly one day from the last run; 
        # see https://docs.databricks.com/api/workspace/jobs/create#trigger
        periodic:
          interval: 1
          unit: DAYS
      email_notifications:
        on_failure:
          - some_email@some_domain.com
      job_clusters:
        - job_cluster_key: job_cluster
          new_cluster:
            spark_version: 15.4.x-scala2.12
            node_type_id: i3.xlarge
            autoscale:
              min_workers: 1
              max_workers: 1
      tasks:
        - task_key: query1_sparqlin
          # existing_cluster_id: ${var.cluster_id} # Existing cluster can be used instead
          job_cluster_key: job_cluster
          libraries:
            - pypi:
                package: sparqlin==0.1.11  # Install your package via PyPI (or custom repository)
            # - whl: ../dist/*.whl         # Alternatively, you can upload the sparqlin wheel into Volume
          python_wheel_task:
            package_name: "sparqlin"       # Package name as defined in your setup.py or pyproject.toml
            entry_point: "sparqlin"        # Entry point defined in the package
            named_parameters:
              sql-query-path: "${workspace.root_path}/files/sql/query1.sql"
              table-name: "sparkdev.default.taxi_top_five"
        - task_key: query2_sparqlin
          depends_on:
            - task_key: query1_sparqlin
          # existing_cluster_id: ${var.cluster_id} # Existing cluster can be used instead
          job_cluster_key: job_cluster
          libraries:
            - pypi:
                package: sparqlin==0.1.11  # Install your package via PyPI (or custom repository)
            # - whl: ../dist/*.whl         # Alternatively, you can upload the sparqlin wheel into Volume
          python_wheel_task:
            package_name: "sparqlin"       # Package name as defined in your setup.py or pyproject.toml
            entry_point: "sparqlin"        # Entry point defined in the package
            named_parameters:
              sql-query-path: "${workspace.root_path}/files/sql/query2.sql"
              table-name: "sparkdev.default.taxi_count"
        # You can also continue `tasks` to use other frameworks or task types that Databricks support
```

### Example Spark SQL transformation (sql/query.sql)
```sparksql
SELECT * FROM samples.nyctaxi.trips LIMIT 5;
```

### Example Usage of Testing framework
#### Test Parameterized Dataset Paths
This example tests loading datasets into Spark DataFrames from YAML configuration files. It uses `pytest` fixtures 
to dynamically provide the `datasets_path`.
```python
from sparqlin.testing.helpers import get_spark_dataframe


@pytest.mark.parametrize("datasets_path", ["tests/testing/datasets_test/datasets.yml"], indirect=True)
def test_base_test_config(spark_session, datasets_path):
    # Load test table as DataFrame
    test_table_df = get_spark_dataframe(spark_session, datasets_path, "testdb.test_table")
    second_table_df = get_spark_dataframe(spark_session, datasets_path, "testdb.second_table")

    # Validate record counts
    assert test_table_df.count() == 3
    assert second_table_df.count() == 2
```
#### Configuring and Testing Temporary Hive Tables
This example demonstrates how to use `BaseTestConfig` to register tables as temporary datasets in Spark and perform SQL operations.
```python
from sparqlin.testing.base_test_config import BaseTestConfig


def test_hive_table_operations(hive_data_yaml, tmp_path_factory):
    datasets_file, tmp_path = hive_data_yaml

    # Initialize BaseTestConfig
    config = BaseTestConfig(tmp_path_factory)

    # Set datasets location
    config.DATASETS_LOCATION = datasets_file

    # Create Spark session
    spark = config.create_spark_session()

    # Register tables from YAML file
    config.register_tables(spark)

    # Verify table registration
    test_table_df = spark.sql("SELECT * FROM testdb.test_table")
    second_table_df = spark.sql("SELECT * FROM testdb.second_table")
    assert test_table_df.count() == 3

    # Perform join operation
    joined_df = test_table_df.join(second_table_df, test_table_df.id == second_table_df.id)
    joined_results = joined_df.select("name", "value").collect()
    assert len(joined_results) == 2
    assert any(row.name == "Alice" and row.value == 100 for row in joined_results)

```

***

## Development Setup
To contribute or set up a local development environment for `sparqlin`, follow these steps:
1. Clone the repository:
   ```Bash
   git clone https://gitlab.com/rokorolev/sparqlin.git
   cd sparqlin
   ```
2. Install dependencies:
   ```Bash
   pip install -r requirements.txt
   ```
3. Run the tests:
   The framework uses `pytest` for testing. You can run the test suite as follows:
   ```Bash
   pytest
   ```

## Build the Package
1. Install Build Tools
   `pip install setuptools wheel`
2. Build the Package
   ```
   rm -rf build dist *.egg-info
   python setup.py sdist bdist_wheel
   ```
## Upload the Package to PyPi
1. Install Twine
   `pip install twine`
2. Generate token for PyPi account
3. Upload the Package
   `twine upload dist/*`

***

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
## Contributions
Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request. 
Please ensure proper test coverage for new functionality.
## Issues
If you encounter a bug or have a feature request, please open an issue on the project's [GitLab repository](https://gitlab.com/rokorolev/sparqlin).
## Author
Developed and maintained by [Roman Korolev](https://rokorolev.gitlab.io/).