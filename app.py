import os
import time
import sys
import threading

from kafka_monitor.consumer import Consumer
from kafka_monitor.producer import Producer
from utils.config import Config
from utils.file import File
from utils.utils import Utils


def start_mointoring(monitors: list, producer: Producer, consumer: Consumer):

    if not len(monitors):
        return 
    
    for task in monitors:
        
        #Validate URL
        if 'url' not in task:
            print("CORRUPTED_URL_VALUE_ERROR with item => " + str(task))
            continue
        
        if not Utils.is_valid_URL(task['url']):
            print("PARSE_URL_ERROR", task['url'])
            continue

        producer.append_task(task)
    
    consumer.start()
    
    # make sure the consumer is ready with setting up db etc. 
    # before start producing
    while not consumer.is_ready():
        print("consumer not ready yet .. ")
        time.sleep(1)

    producer.start()

def stop_monitor(producer: Producer, consumer: Consumer):
    if not producer or not consumer:
        return

    producer.stop()
    consumer.stop()
    
def run(topic: str, db: str, table: str, filepath=None):
    if not filepath:
        filepath = Config.MONITERFILE
    
    interval = File.read_time_interval(filepath)
    monitors = File.read_monitors(filepath)
        
    producer = Producer(topic, interval)

    consumer = Consumer(topic, db, table)

    start_mointoring(monitors, producer, consumer)

    return producer, consumer

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(Config.K_MONITOR_TOPIC,
            Config.PS_DATABASE_NAME,
            Config.PS_WEBSITE_TABLE_NAME,
            sys.argv[1])
    else:
        run(Config.K_MONITOR_TOPIC,
            Config.PS_DATABASE_NAME,
            Config.PS_WEBSITE_TABLE_NAME)