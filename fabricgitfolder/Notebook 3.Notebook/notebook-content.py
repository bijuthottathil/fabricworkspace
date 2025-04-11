# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5003e904-9e23-41f9-b9dc-2df7f05e304c",
# META       "default_lakehouse_name": "bijulakehouse",
# META       "default_lakehouse_workspace_id": "c1625ff0-b7f2-4bde-a31b-03b7f7e67e04",
# META       "known_lakehouses": [
# META         {
# META           "id": "5003e904-9e23-41f9-b9dc-2df7f05e304c"
# META         }
# META       ]
# META     }
# META   }
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
