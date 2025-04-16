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


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Initialize Spark session
spark = SparkSession.builder.getOrCreate()

# Define schema
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# Sample data
data = [
    (1, "Alice", 25),
    (2, "Bob", 30),
    (3, "Cathy", 28)
]

# Create a DataFrame
df = spark.createDataFrame(data, schema=schema)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# Save the dataframe as a delta table
df.write.format("delta").saveAsTable("mytable")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from mytable

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Path to the Delta table in the Lakehouse
delta_table_path = "Files/biju_table"

# Write the DataFrame as a Delta table
df.write.format("delta").mode("overwrite").save(delta_table_path)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

delta_df = spark.read.format("delta").load(delta_table_path)
delta_df.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE my_table USING DELTA LOCATION 'Files/biju_table';

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from my_table

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp
import time
from datetime import datetime
import uuid

# SparkSession is already initialized in Fabric notebooks, but we include it for clarity
spark = SparkSession.builder.getOrCreate()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Simulating a DataFrame that generates 100 streaming events
def generate_events():
    for i in range(1, 101):
        yield {"event_id": str(uuid.uuid4()), 
               "event": f"event_{i}", 
               "timestamp": datetime.now()}

# Create a Spark DataFrame from the generated events
event_rdd = spark.sparkContext.parallelize(list(generate_events()))
event_df = spark.createDataFrame(event_rdd)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Define Delta table path in your Fabric Lakehouse
delta_table_path = "Files/events_delta_table"

# Write the events DataFrame to a Delta table
event_df.write.format("delta").mode("overwrite").save(delta_table_path)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE events_delta_table  USING DELTA LOCATION 'Files/events_delta_table';

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC select * from events_delta_table

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE salesorders
# MAGIC (
# MAGIC     Orderid INT NOT NULL,
# MAGIC     OrderDate TIMESTAMP NOT NULL,
# MAGIC     CustomerName STRING,
# MAGIC     SalesTotal FLOAT NOT NULL
# MAGIC )
# MAGIC USING DELTA

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
