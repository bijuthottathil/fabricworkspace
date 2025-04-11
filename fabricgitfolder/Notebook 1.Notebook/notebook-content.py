# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!!
!pip install pydeequ


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("PyDeequ Example") \
    .config("spark.jars.packages", "com.amazon.deequ:deequ:2.0.0-spark-3.0-scala-2.12") \
    .getOrCreate()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data = spark.createDataFrame([
    ("Alice", 34),
    ("Bob", 45),
    (None, 29)
], ["name", "age"])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("PyDeequ Example") \
    .config("spark.jars.packages", "com.amazon.deequ:deequ:2.0.0-spark-3.0-scala-2.12") \
    .getOrCreate()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# conftest.py
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("pytest-pyspark") \
        .getOrCreate()
    yield spark
    spark.stop()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# test_dataframe.py
def test_dataframe_count(spark):
    # Create a sample DataFrame
    data = [("Alice", 34), ("Biob", 45)]
    df = spark.createDataFrame(data, ["name", "age"])
    
    # Check that the DataFrame has the expected count
    assert df.count() == 2

def test_dataframe_filter(spark):
    # Create a sample DataFrame
    data = [("Alice", 34), ("Biob", 35)]
    df = spark.createDataFrame(data, ["name", "age"])
    
    # Filter the DataFrame for rows where age is greater than 40
    filtered_df = df.filter(df.age > 40)
    results = filtered_df.collect()
    
    # Expect only one row (Bob)
    assert len(results) == 1
    assert results[0]["name"] == "Bob"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def test_force_failure(spark):
    data = [("Alice", 34), ("Bob", 45)]
    df = spark.createDataFrame(data, ["name", "age"])
    # Intentionally set an incorrect expected count to force a failure.
    expected_column_count = 3
    actual_column_count = len(df.columns)
    assert actual_column_count == expected_column_count, f"Expected {expected_column_count} columns, but got {actual_column_count}"

    

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def test_dataframe_column_count(spark):
    # Create a sample DataFrame
    data = [("Alice", 34), ("Bob", 45)]
    df = spark.createDataFrame(data, ["name", "age"])
    
    # Validate that the DataFrame has exactly 2 columns
    expected_column_count = 3
    actual_column_count = len(df.columns)
    assert actual_column_count == expected_column_count, f"Expected {expected_column_count} columns, but got {actual_column_count}"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

    # tests/test_my_spark_app.py
    from my_spark_app import process_data  # Assuming your PySpark code is in my_spark_app.py
    from chispa.dataframe_comparer import assert_df_equality
    import pytest
    from pyspark.sql import Row
    
    
    def test_process_data(spark):
        input_data = [("Alice", 30), ("Bob", 25)]
        input_df = spark.createDataFrame(input_data, ["name", "age"])
    
        expected_data = [("Alice", 30, "Adult"), ("Bob", 25, "Adult")]
        expected_df = spark.createDataFrame(expected_data, ["name", "age", "category"])
    
        result_df = process_data(input_df)
    
        assert_df_equality(result_df, expected_df, ignore_row_order=True, ignore_column_order=True)
    
    
    def test_empty_dataframe(spark):
        empty_df = spark.createDataFrame([], schema="name STRING, age INT")
        result_df = process_data(empty_df)
        assert result_df.count() == 0
    
    
    @pytest.mark.parametrize(
        "input_data, expected_category",
        [
            ([("Charlie", 15)], "Teenager"),
            ([("David", 65)], "Senior"),
            ([("Eve", 35)], "Adult"),
        ],
    )
    def test_category_assignment(spark, input_data, expected_category):
        input_df = spark.createDataFrame(input_data, ["name"])
        
        # Create a DataFrame with sample data
        data = [Row(name="Alice", age=30), Row(name="Bob", age=25), Row(name="Charlie", age=15), Row(name="David", age=65)]
        df = spark.createDataFrame(data)
    
        # Define the function to categorize based on age
        def categorize_age(age):
            if age < 18:
                return "Teenager"
            elif age >= 60:
                return "Senior"
            else:
                return "Adult"
    
        # Register the UDF
        categorize_age_udf = udf(categorize_age, StringType())
        
        # Apply the UDF to create a new column
        df_with_category = df.withColumn("category", categorize_age_udf(df["age"]))
        
        # Filter the DataFrame based on the expected category
        filtered_df = df_with_category.filter(df_with_category["category"] == expected_category)
        
        # Check if the filtered DataFrame is empty
        assert filtered_df.count() > 0
    
    
    @pytest.mark.xfail
    def test_failing_test(spark):
        # This test is intentionally designed to fail.
        data = [("Alice", 30), ("Bob", 25)]
        df = spark.createDataFrame(data, ["name", "age"])
        assert df.count() == 3

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
