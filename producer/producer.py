import requests
from bs4 import BeautifulSoup
import json
import time
from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer

class WebScraperProducer:
    def __init__(self, url, kafka_server, topic):
        self.url = url
        self.kafka_server = kafka_server
        self.topic = topic
        self.producer = self.create_producer()
        self.data = []

    def create_producer(self):
        retries = 10
        for i in range(retries):
            try:
                producer = KafkaProducer(
                    bootstrap_servers=self.kafka_server,
                    api_version=(0, 11, 5),
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                return producer
            except NoBrokersAvailable:
                print(f"Attempt {i+1}/{retries} - Kafka broker not available")
                time.sleep(5)
        raise Exception("Failed to connect to Kafka broker after several attempts")

    def fetch_product_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products_ul = soup.find('ul', class_='products columns-4')
        products_li = products_ul.find_all('li')

        for product in products_li:
            href = product.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
            product_response = requests.get(href)
            product_soup = BeautifulSoup(product_response.text, 'html.parser')
            product_div = product_soup.find('div', class_='summary entry-summary')

            title = product_div.find('h1', class_='product_title entry-title').text.strip()
            price = product_div.find('p', class_='price').text.strip()
            description = product_div.find('div', class_='woocommerce-product-details__short-description').text.strip()
            stock = product_div.find('p', class_='stock in-stock').text.strip()

            self.data.append({'name': title, 'price': price, 'description': description, 'stock': stock})

        print('Data Gathered')

    def send_to_kafka(self):
        for item in self.data:
            self.producer.send(self.topic, item)
            time.sleep(1)
        self.producer.flush()

    def run(self):
        self.fetch_product_data()
        self.send_to_kafka()

if __name__ == "__main__":
    scraper_producer = WebScraperProducer(
        url="https://scrapeme.live/shop/",
        kafka_server='kafka:19092',
        topic='my-topic'
    )
    scraper_producer.run()
