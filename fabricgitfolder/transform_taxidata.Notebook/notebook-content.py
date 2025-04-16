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

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

taxi_df = spark.sql("SELECT * FROM bijulakehouse.NewYorkTaxiTable LIMIT 1000")
display(taxi_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

taxi_df.createOrReplaceTempView("taxi_data")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


filtered_df_sql = spark.sql("""
    SELECT
        VendorID,
        lpepPickupDatetime,
        lpepDropoffDatetime,
        tripDistance,
        totalAmount
    FROM taxi_data
    WHERE tripDistance > 2 AND totalAmount > 10
""")
filtered_df_sql.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col,expr

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# Basic Transformation 2: Add a Derived Column
# Using Spark SQL
derived_df_sql = spark.sql("""
    SELECT *,
           totalAmount / tripDistance AS fare_per_mile
    FROM taxi_data
    WHERE tripDistance > 0
""")
derived_df_sql.show()



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Using PySpark API
derived_df_pyspark = taxi_df.filter(col("tripDistance") > 0).withColumn(
    "fare_per_mile", col("totalAmount") / col("tripDistance")
)
display(derived_df_pyspark)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************



# Basic Transformation 3: Aggregate Data
# Using Spark SQL
aggregated_df_sql = spark.sql("""
    SELECT paymentType,
           COUNT(*) AS trip_count,
           AVG(totalAmount) AS avg_total_amount,
           AVG(tripDistance) AS avg_trip_distance
    FROM taxi_data
    GROUP BY paymentType
""")
aggregated_df_sql.show()



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Using PySpark API
aggregated_df_pyspark = taxi_df.groupBy("paymentType").agg(
    expr("COUNT(*)").alias("trip_count"),
    expr("AVG(totalAmount)").alias("avg_total_amount"),
    expr("AVG(tripDistance)").alias("avg_trip_distance")
)
aggregated_df_pyspark.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Define the path where the Delta table will be stored
delta_table_path = "Files/aggregated_taxi_data"

# Write the aggregated DataFrame to a Delta table
aggregated_df_pyspark.write.format("delta").mode("overwrite").save(delta_table_path)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE aggregated_taxi_data
# MAGIC USING DELTA
# MAGIC LOCATION 'Files/aggregated_taxi_data';


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from aggregated_taxi_data

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from aggregated_taxi_data

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

