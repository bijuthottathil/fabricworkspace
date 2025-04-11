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
# META       "default_lakehouse_workspace_id": "c1625ff0-b7f2-4bde-a31b-03b7f7e67e04"
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
from pyspark.sql import functions as F
# Import Delta Lake API for merge/upsert
from delta.tables import DeltaTable

# Define paths
csv_folder_path = "/mnt/data/sample_csv_files/"  # Replace with your folder path (local or DBFS)
delta_table_path = "/mnt/delta/target_table"       # Replace with your Delta table path

# Read multiple CSV files from the folder into a single DataFrame
# Assumes CSV files have headers
batchDF = spark.read.option("header", "true").csv(csv_folder_path)

# (Optional) Cast columns if necessary, for example, ensuring id is an integer
batchDF = batchDF.withColumn("id", F.col("id").cast("int"))

# Check if the target Delta table already exists
if DeltaTable.isDeltaTable(spark, delta_table_path):
    # Load existing Delta table
    deltaTable = DeltaTable.forPath(spark, delta_table_path)
    
    # Perform merge/upsert based on the 'id' column
    deltaTable.alias("tgt").merge(
        source = batchDF.alias("src"),
        condition = "tgt.id = src.id"
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()
    
    print("Upsert completed on the Delta table.")
else:
    # If the Delta table does not exist, create it
    batchDF.write.format("delta").save(delta_table_path)
    print("Delta table created.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************


# CELL ********************

from pyspark.sql import functions as F

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


csv_folder_path = "Files/csvfiles/"  # Replace with your folder path (local or DBFS)
delta_table_path = "Files/Destinatiion/abc/"       # Replace with your Delta table path
batchDF = spark.read.option("header", "true").csv(csv_folder_path)
batchDF.write.mode("overwrite").format("delta").save(delta_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import Delta Lake API for merge/upsert
from delta.tables import DeltaTable

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# Check if the target Delta table already exists

    # If the Delta table does not exist, create it
    batchDF.write.format("delta").save(delta_table_path)
    print("Delta table created.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").load("Files/csvfiles/customers-100.csv")
# df now is a Spark DataFrame containing CSV data from "Files/csvfiles/customers-100.csv".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Step 2: Write DataFrame to a Delta table
csv_folder_path = "Files/csvfiles/"  # Replace with your folder path (local or DBFS)
delta_table_path = "Files/Destination/"       # Replace with your Delta table path
batchDF = spark.read.option("header", "true").csv(csv_folder_path)

batchDF.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(delta_table_path)
print("CSV data written to Delta table.")

# Step 3: Read the Delta table and display its contents
deltaDF = spark.read.format("delta").load(delta_table_path)
display(deltaDF)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
