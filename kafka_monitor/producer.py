import threading
import multiprocessing
import json
import time
import sys
import datetime
from threading import Thread
from kafka import KafkaProducer
from utils.config import Config
from utils.network import Network

class Producer(threading.Thread):

    def __init__(self, topic: str, interval: int):
        self.interval = interval
        self.topic = topic
        self.tasks = []
        self.worker_queue = []
        threading.Thread.__init__(self)

        if Config.is_test():
            threading.Thread.daemon = True

        self.stop_event = threading.Event()

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
        i = 1
        
        pool = multiprocessing.Pool()
        last_time_called = datetime.datetime.now()
        while not self.stop_event.is_set():

            # information logging
            print("Iteration no. => " + str(i))
            print("Currunt active thread count => " + str(threading.active_count()))
            print("last iteration called since (time delta)=> " + str(datetime.datetime.now() - last_time_called))
            last_time_called = datetime.datetime.now()

            if self.stop_event.is_set():
                break

            pool.map_async(Network.get_website_status, self.tasks, callback=self.send_results)

            i += 1
            time.sleep(self.interval)

        # block at this line until all processes are done
        pool.close()
        pool.join()
        self.producer.close()
        print("Producer of \"" + self.topic + "\" is stopped!")
    
    def get_message_count(self):
        return self.message_count

    def send_results(self, res):
        results = []
        results.extend(res)

        for website_status in results:
            if website_status:
                self.producer.send(self.topic, website_status)

                print("\nProducer sends ", end="")

                if website_status['name']:
                    print(website_status['name'])

                print(str(website_status))

                self.message_count += 1