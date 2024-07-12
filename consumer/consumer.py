from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time
import json
import os

class KafkaDataConsumer:
    def __init__(self, topic, kafka_server, output_file):
        self.topic = topic
        self.kafka_server = kafka_server
        self.output_file = output_file
        self.consumer = self.create_consumer()
        self.messages = []

    def create_consumer(self):
        retries = 10
        for i in range(retries):
            try:
                consumer = KafkaConsumer(
                    self.topic,
                    bootstrap_servers=self.kafka_server,
                    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
                )
                return consumer
            except NoBrokersAvailable:
                print(f"Attempt {i+1}/{retries} - Kafka broker not available")
                time.sleep(5)
        raise Exception("Failed to connect to Kafka broker after several attempts")

    def consume_messages(self):
        for message in self.consumer:
            self.messages.append(message.value)
            print(f'Received: {message.value}')
            self.write_to_file()

    def write_to_file(self):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, indent=4)

    def run(self):
        self.consume_messages()

if __name__ == "__main__":
    consumer = KafkaDataConsumer(
        topic='my-topic',
        kafka_server='kafka:19092',
        output_file='../data/data.json'
    )
    consumer.run()
