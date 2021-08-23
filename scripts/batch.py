import os
import sys

import yaml
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


class BatchLayer:

    def __init__(self):
        abs_path = os.path.abspath(sys.argv[0])
        with open(os.path.join(os.path.dirname(abs_path), 'spark-config.yaml'), 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader) or {}
        self.speed_config = config.get('batch')
        sc = SparkContext(
            "{}[{}]".format(self.speed_config.get('mode'), self.speed_config.get('num_threads')),
            self.speed_config.get('name'))
        self.ssc = StreamingContext(sc, self.speed_config.get('batch_interval'))

    def run(self):
        self.ssc.start()


if __name__ == '__main__':
    BatchLayer().run()
