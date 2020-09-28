import unittest 
import sys
import os
import time
sys.path.append("..")
import app

from kafka_client.Consumer import Consumer
from kafka_client.Producer import Producer
from config import Config

class test_CorruptedMonitorFileValidation(unittest.TestCase):

    def test_b_corrupted_monitor_file(self):
        
        self.assertRaises(Exception, lambda: app.run(Config.K_MONITOR_TOPIC,
                                                Config.PS_DATABASE_NAME,
                                                Config.PS_USERNAME,
                                                Config.PS_PASSWORD,
                                                Config.PS_HOST,
                                                Config.PS_PORT,
                                                Config.PS_TEST_WEBSITE_TABLE_NAME,
                                                True,
                                                "tests/t_monitor_corrupted_interval.yaml"))
    def test_a_corrupted_monitor_file(self):
            prod, cons = app.run(Config.K_MONITOR_TOPIC,
                                Config.PS_DATABASE_NAME,
                                Config.PS_USERNAME,
                                Config.PS_PASSWORD,
                                Config.PS_HOST,
                                Config.PS_PORT,
                                Config.PS_TEST_WEBSITE_TABLE_NAME,
                                True,
                                "tests/t_monitor_corrupted.yaml")
            time.sleep(10)
            app.stop_monitor(prod, cons)
            print("Uncorrupted url= " + str(Producer.get_message_count()))
            self.assertEqual(Producer.get_message_count(), Consumer.get_message_count())

if __name__ == '__main__': 
    unittest.main() 