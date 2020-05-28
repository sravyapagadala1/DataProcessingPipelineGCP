from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_TOPIC_NAME_CONS = "transmsg"
KAFKA_BOOTSTRAP_SERVERS_CONS = '35.238.42.190:9092'

if __name__ == "__main__":
    print("Real-Time Data Pipeline Started ...")

    spark = SparkSession \
        .builder \
        .appName("Real-Time Data Pipeline Demo") \
        .master("local[*]") \
        .config("spark.jars", "file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//spark-sql-kafka-0-10_2.11-2.4.0.jar,file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//kafka-clients-2.0.0.jar") \
        .config("spark.executor.extraClassPath", "file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//spark-sql-kafka-0-10_2.11-2.4.0.jar:file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//kafka-clients-2.0.0.jar") \
        .config("spark.executor.extraLibrary", "file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//spark-sql-kafka-0-10_2.11-2.4.0.jar:file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//kafka-clients-2.0.0.jar") \
        .config("spark.driver.extraClassPath", "file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//spark-sql-kafka-0-10_2.11-2.4.0.jar:file:///C://Users//sravy//Documents//Projects//DataProcessingPipeline//jar_files//kafka-clients-2.0.0.jar") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Construct a streaming DataFrame that reads from transmsg
    transaction_detail_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
        .option("subscribe", KAFKA_TOPIC_NAME_CONS) \
        .option("startingOffsets", "latest") \
        .load()

    print("Printing Schema of transaction_detail_df: ")
    transaction_detail_df.printSchema()

    # Write result dataframe into console for debugging purpose
    trans_detail_write_stream = transaction_detail_df \
        .writeStream \
        .trigger(processingTime='5 seconds') \
        .outputMode("update") \
        .option("truncate", "false")\
        .format("console") \
        .start()

    trans_detail_write_stream.awaitTermination()

    print("Real-Time Data Pipeline Completed.")