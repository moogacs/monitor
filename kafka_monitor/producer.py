import threading
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
        
        # do the work in a different thread to make sure there is no time delay inside the main loop
        # the used approach is to create a worker thread with worker queue which is responsible to check taget websites 
        # then let the producers send the results

        # to make sure the target wesbites is checked in the correct time periodically, re-fill
        # the worker queue after the time interval 
        worker_thread = Thread(target = self.tagerts_checker_worker)
        worker_thread.daemon = True
        

        while not self.stop_event.is_set():
            print("iteration no. => " + str(i))
            print("Currunt active thread count => " + str(threading.active_count()))

            if self.stop_event.is_set():
                break

            # fill the tasks queue with websites
            for task in self.tasks:
                self.worker_queue.append(task)
            
            if not worker_thread.is_alive():
                worker_thread.start()

            i += 1
            time.sleep(self.interval)

        self.producer.close()
        print("Producer of \"" + self.topic + "\" is stopped!")
    
    def get_message_count(self):
        return self.message_count

    def tagerts_checker_worker(self):
        while True:
            if self.stop_event.is_set():
                break
            
            # pop from the queue, then process, then send
            if self.worker_queue:
                task = self.worker_queue.pop(0)
                pattern = None
                name = ""

                if 'pattern' in task:
                    pattern = task['pattern']

                if 'name' in task:
                    name = task['name']

                if 'url' not in task:
                    print("CORRUPTED_URL_VALUE_ERROR with item => " + str(task))
                    continue

                if self.stop_event.is_set():
                    break
                
                website_status = Network.get_website_status(name, task['url'], pattern)

                if website_status:
                    self.message_count += 1
                    print("\nProducer sends " + website_status['name']+ " \n"+ str(website_status))
                    self.producer.send(self.topic, website_status)