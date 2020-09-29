import unittest 
import sys
import os
import time
import app

from kafka_monitor.consumer import Consumer
from kafka_monitor.producer import Producer
from utils.config import Config
from utils.file import File

# TODO test shoudld have setUP & tearDown but ignored for simplicity

class test_ProducerEqualConsumer(unittest.TestCase):

    def test_producer_equal_consumer(self):
        prod, cons = app.run(Config.K_MONITOR_TOPIC,
                            Config.PS_DATABASE_NAME,
                            Config.PS_USERNAME,
                            Config.PS_PASSWORD,
                            Config.PS_HOST,
                            Config.PS_PORT,
                            Config.PS_TEST_WEBSITE_TABLE_NAME,
                            True)

        interval = File.read_time_interval()

        time.sleep(interval)

        app.stop_monitor(prod, cons)

        self.assertEqual(prod.get_message_count(), cons.get_message_count())

if __name__ == '__main__': 
    unittest.main() 