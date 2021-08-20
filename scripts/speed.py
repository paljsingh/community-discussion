import os
import sys

import yaml
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


class SpeedLayer:

    def __init__(self):
        abs_path = os.path.abspath(sys.argv[0])
        with open(os.path.join(os.path.dirname(abs_path), 'spark-config.yaml'), 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader) or {}
        sc = SparkContext("local[2]", "NetworkWordCount")
        ssc = StreamingContext(sc, 1)