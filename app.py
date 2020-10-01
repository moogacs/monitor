import os
import time
import sys
import threading

from kafka_monitor.consumer import Consumer
from kafka_monitor.producer import Producer
from utils.config import Config
from utils.file import File
from utils.utils import Utils


def start_mointoring(monitor_file: str, producer: Producer, consumer: Consumer):

    monitors =  monitor_file['monitors']
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

def run(topic: str, db: str, table: str, filepath=None):
    if filepath:
        monitor_file = File.read_yaml_monitor_file(filepath)
    else:
        monitor_file = File.read_yaml_monitor_file()

    if 'interval' not in monitor_file:
        raise Exception('INTERVAL_NOT_FOUND')
        return

    if 'monitors' not in monitor_file:
        raise Exception('MONITORS_NOT_FOUND')
        return

    interval =  monitor_file['interval']

    producer = Producer(topic, interval)

    consumer = Consumer(topic, db, table)

    start_mointoring(monitor_file, producer, consumer)

    return producer, consumer

def stop_monitor(producer, consumer):
    if not producer or not consumer:
        return

    producer.stop()
    consumer.stop()

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