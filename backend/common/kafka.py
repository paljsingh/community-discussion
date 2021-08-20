from kafka import KafkaClient, KafkaProducer

from common.config import Config


class Kafka(KafkaClient):
    config = Config.load()

    def __init__(self):
        super().__init__(hosts=str.join(',', self.config.get('kafka_endpoints')))

    def get_producer(self, topic: bytes):
        return self.topics[topic].get_producer()
