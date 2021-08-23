import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, DoubleType


class SpeedLayer:

    def __init__(self):
        spark = SparkSession.builder.appName("streamer").getOrCreate()
        df_in = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "posts,users,communities,videos,images") \
            .load()

        df_in \
            .writeStream \
            .format("console") \
            .trigger(processingTime='1 seconds') \
            .start() \
            .awaitTermination()


if __name__ == '__main__':
    os.environ['PYSPARK_SUBMIT_ARGS'] = \
        '--jars ' \
        + 'var/jars/spark-sql-kafka-0-10_2.12-3.0.1.jar,' \
        + 'var/jars/kafka-clients-2.4.1.jar,' \
        + 'var/jars/spark-streaming-kafka-0-10-assembly_2.12-3.0.1.jar,' \
        + 'var/jars/commons-pool2-2.6.2.jar' \
        + ' pyspark-shell'
    #     + 'var/jars/spark-tags_2.12-3.0.1.jar,' \
    #     + 'var/jars/spark-token-provider-kafka-0-10_2.12-3.0.1.jar,' \
    SpeedLayer()
