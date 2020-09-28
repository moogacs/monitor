import threading
import json
import re
import time
import sys
import requests
import datetime

from kafka import KafkaProducer
from config import Config

class Producer(threading.Thread):
    message_count = 0

    def __init__(self, topic: str, interval: int):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        self.stop_event = threading.Event()
        self.interval = interval
        self.topic = topic
        self.tasks = []
        
        Producer.message_count = 0
            
    def append_task(self, task: dict):
        self.tasks.append(task)

    def stop(self):
        self.producer.close()
        print("Producer stopped!")
        self.stop_event.set()

    def run(self):
        print("Producer runs!")
        Producer.producer = KafkaProducer(bootstrap_servers=[Config.K_HOST + ':' + Config.K_PORT],
                                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                    security_protocol=Config.K_SECURITY_PROTOCOL,
                                    ssl_cafile=Config.K_SSL_CAT_FILE,
                                    ssl_certfile=Config.K_SSL_CERT_FILE,
                                    ssl_keyfile=Config.K_SSL_KEY_FILE)
        
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

                website_status = self.get_status(name, task['url'], pattern)
                if website_status:
                    Producer.message_count += 1
                    print("\nProducer sends " + website_status['name']+ " \n"+ str(website_status))
                    self.producer.send(self.topic, website_status)

            time.sleep(self.interval)
    
    def get_message_count():
        return Producer.message_count

    def get_status(self, name, url, pattern):
        has_pattern = False
        
        if not bool(re.match(Config.REGEX_URL, url)):
            print("PARSE_URL_ERROR with URL => " + url)
            return

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            response_time = str(round(response.elapsed.total_seconds(),2))
            status_code = response.status_code
            reason = response.reason
            
            if pattern:
                has_pattern = bool(re.search(pattern, response.text))
            
        except requests.exceptions.ConnectionError:
            status_code = "503"
            reason = 'ConnectionError'
            response_time = 0
        except requests.exceptions.HTTPError:
            status_code = "000"
            reason = 'ConnectionError'
            response_time = 0
            
        website_log = {
            "name": name,
            "website": url,
            "status_code":  status_code,
            "reason": reason,
            "response_time": response_time,
            "pattern": pattern,
            "has_pattern": has_pattern
        }

        return website_log