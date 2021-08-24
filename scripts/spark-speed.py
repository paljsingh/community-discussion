import os
import sys
import yaml
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import split


class SpeedLayer:

    def __init__(self, topic):
        self.topic = topic

        spark = SparkSession.builder.appName("streamer").getOrCreate()
        df_in = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", topic) \
            .load()

        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "etc/spark-config.yaml")
        with open(conf_file_path, 'r') as fh:
            self.conf = yaml.load(fh, Loader=yaml.FullLoader)

        df_in \
            .writeStream \
            .trigger(processingTime='{} seconds'.format(self.conf['speed']['batch_interval'])) \
            .foreachBatch(self.write_to_console_and_elasticsearch) \
            .start() \
            .awaitTermination()

    def write_to_console_and_elasticsearch(self, batch_df: DataFrame, batch_id):

        modified_df = batch_df
        for i, field in enumerate(self.conf['topics'][self.topic]['fields']):
            modified_df = modified_df.withColumn(field, split(batch_df['value'], ',').getItem(i))

        modified_df.show()
        modified_df.write \
            .format("org.elasticsearch.spark.sql") \
            .mode('append') \
            .option("checkpointLocation", self.conf['speed']['checkpoint_dir']) \
            .option('es.index.auto.create', 'true') \
            .option("es.nodes.wan.only", 'true') \
            .option('es.resource', '{}/doc'.format(self.topic)) \
            .option("es.nodes", self.conf['sink']['host']) \
            .option("es.port", self.conf['sink']['port']) \
            .option("header", "true") \
            .save()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("usage: {} <topic>".format(sys.argv[0]))
        sys.exit(1)

    tp = sys.argv[1]
    jars = ','.join('var/jars/{}'.format(x) for x in [
        'commons-pool2-2.6.2.jar',
        'spark-streaming-kafka-0-10-assembly_2.12-3.0.1.jar',
        'kafka-clients-2.4.1.jar',
        'spark-sql-kafka-0-10_2.12-3.0.1.jar',
        'elasticsearch-spark-20_2.12-7.14.0.jar',
    ])
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars {} pyspark-shell'.format(jars)
    SpeedLayer(tp)
