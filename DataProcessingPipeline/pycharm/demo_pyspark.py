from pyspark.sql import SparkSession

# Import Required PySpark Packages
from pyspark.sql import SparkSession

if __name__ == "__main__":
    print("Application Started ...")

    spark = SparkSession \
            .builder \
            .appName("First PySpark Demo") \
            .master("local[*]") \
            .getOrCreate()

    input_file_path = "file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//pycharm//sample_data//tech.txt"

    tech_rdd = spark.sparkContext.textFile(input_file_path)

    print("Printing data in the tech_rdd: ")
    print(tech_rdd.collect())

    print("Application Completed.")
