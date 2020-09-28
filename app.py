import yaml
import os
import time
import sys
import threading

from kafka_client.Consumer import Consumer
from kafka_client.Producer import Producer
from config import Config


def read_yaml_monitor_file(filepath=None):
    if not filepath:
        filepath = "monitor.yml"

    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print(error)


def start_mointoring(monitor_file, producer, consumer):
    monitors =  monitor_file['monitors']
    consumer.start()
    
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
            print("Error parsing yaml file, has no url")
            continue

        producer.append_task(website_task)
    time.sleep(1)
    producer.start()

if len(sys.argv) > 1:
    filepath = sys.argv[1]

def run(topic, db, user, pw, host, port, table, is_test, filepath=None):
    if filepath:
        monitor_file = read_yaml_monitor_file(filepath)
    else:
        monitor_file = read_yaml_monitor_file()

    if 'interval' not in monitor_file:
        raise Exception('INTERVAL_NOT_FOUND')
        return
    if 'monitors' not in monitor_file:
        raise Exception('MONITORS_NOT_FOUND')
        return

    interval =  monitor_file['interval']

    producer = Producer(topic, interval, is_test)

    consumer = Consumer(topic, db, user, pw, host, port, table, is_test)

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
            Config.PS_USERNAME,
            Config.PS_PASSWORD,
            Config.PS_HOST,
            Config.PS_PORT,
            Config.PS_WEBSITE_TABLE_NAME,
            False,
            sys.argv[1])
    else:
        run(Config.K_MONITOR_TOPIC,
            Config.PS_DATABASE_NAME,
            Config.PS_USERNAME,
            Config.PS_PASSWORD,
            Config.PS_HOST,
            Config.PS_PORT,
            Config.PS_WEBSITE_TABLE_NAME,
            False)