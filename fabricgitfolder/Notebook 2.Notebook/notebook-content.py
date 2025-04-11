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


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").load("Files/insurance.csv")
# df now is a Spark DataFrame containing CSV data from "Files/insurance.csv".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
