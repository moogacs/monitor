import os
import time
import sys
import threading

from kafka_monitor.consumer import Consumer
from kafka_monitor.producer import Producer
from utils.config import Config
from utils.file import File


def start_mointoring(monitor_file: str, producer: Producer, consumer: Consumer):
    monitors =  monitor_file['monitors']

    for site in monitors:
        website_task = {}
        if 'name' in site:
            name = site['name']
            website_task["name"] = name
        if 'url' in site:
            url = site['url']
            website_task["url"] = url
        if 'pattern' in site:
            pattern = site['pattern']
            website_task["pattern"] = pattern
        
        if not url:
            print("Error parsing yaml file, has no url at => ", str(site))
            continue

        producer.append_task(website_task)
    
    consumer.start()
    
    # make sure the consumer is ready with setting up db etc. 
    # before start producing
    while not consumer.is_ready():
        print("consumer not ready .. ")
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
    if producer:
        producer.stop()
    if consumer:
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