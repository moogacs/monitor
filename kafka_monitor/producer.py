import threading
import json
import time
import sys
import datetime

from kafka import KafkaProducer
from utils.config import Config
from utils.network import Network

class Producer(threading.Thread):

    def __init__(self, topic: str, interval: int, is_test: bool):
        self.interval = interval
        self.topic = topic
        self.tasks = []

        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

        # make thread dies with main thread in case of test env
        if is_test:
            threading.Thread.daemon = True

        self.producer = KafkaProducer(bootstrap_servers=[Config.K_HOST + ':' + Config.K_PORT],
                                        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                        security_protocol=Config.K_SECURITY_PROTOCOL,
                                        ssl_cafile=Config.K_SSL_CAT_FILE,
                                        ssl_certfile=Config.K_SSL_CERT_FILE,
                                        ssl_keyfile=Config.K_SSL_KEY_FILE)

        self.message_count = 0


    def append_task(self, task: dict):
        self.tasks.append(task)

    def stop(self):
        self.stop_event.set()

    def run(self):
        print("Producer runs with topic \"" + self.topic + "\"!")
        while not self.stop_event.is_set():
            for task in self.tasks:
                pattern = None
                name = ""

                if 'pattern' in task:
                    pattern = task['pattern']

                if 'name' in task:
                    name = task['name']

                if 'url' not in task:
                    print("CORRUPTED_URL_VALUE_ERROR with item => " + str(task))
                    continue

                website_status = Network.get_website_status(name, task['url'], pattern)

                if website_status:
                    self.message_count += 1
                    print("\nProducer sends " + website_status['name']+ " \n"+ str(website_status))
                    self.producer.send(self.topic, website_status)
                
                if self.stop_event.is_set():
                    break
                
            time.sleep(self.interval)

        self.producer.close()
        print("Producer of \"" + self.topic + "\" is stopped!")
    
    def get_message_count(self):
        return self.message_count