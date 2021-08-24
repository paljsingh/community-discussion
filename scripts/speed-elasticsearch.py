import os
import sys

import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, DoubleType


class SpeedLayer:

    def __init__(self, topic):
        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "etc/spark-config.yaml")
        with open(conf_file_path, 'r') as fh:
            conf = yaml.load(fh, Loader=yaml.FullLoader)

        spark = SparkSession.builder.appName("streamer").getOrCreate()
        df_in = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", topic) \
            .load()

        df = df_in.drop('_id')
        df.writeStream.format("org.elasticsearch.spark.sql") \
            .option("es.resource", '{}/{}'.format(conf['sink']['index'], conf['sink']['doc_type'])) \
            .option("es.nodes", conf['sink']['host']) \
            .option("es.port", conf['sink']['port']) \
            .start() \
            .awaitTermination()
        # df_in \
        #     .writeStream \
        #     .format("console") \
        #     .trigger(processingTime='1 seconds') \
        #     .start() \
        #     .awaitTermination()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: {} <kafka-topic>".format(sys.argv[0]))

    os.environ['PYSPARK_SUBMIT_ARGS'] = \
        '--jars ' \
        + 'var/jars/spark-sql-kafka-0-10_2.12-3.0.1.jar,' \
        + 'var/jars/kafka-clients-2.4.1.jar,' \
        + 'var/jars/spark-streaming-kafka-0-10-assembly_2.12-3.0.1.jar,' \
        + 'var/jars/commons-pool2-2.6.2.jar,' \
        + 'var/jars/elasticsearch-spark-20_2.10-7.14.0.jar' \
        + ' pyspark-shell'
    #     + 'var/jars/spark-tags_2.12-3.0.1.jar,' \
    #     + 'var/jars/spark-token-provider-kafka-0-10_2.12-3.0.1.jar,' \
    SpeedLayer(sys.argv[1])
