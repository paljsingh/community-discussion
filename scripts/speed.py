import yaml
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


class SpeedLayer:

    def __init__(self):
        with open('./spark-config.yaml', 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader) or {}
        sc = SparkContext("local[2]", "NetworkWordCount")
        ssc = StreamingContext(sc, 1)