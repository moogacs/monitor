import unittest 
import sys
import os
import time
import app

from kafka_monitor.consumer import Consumer
from kafka_monitor.producer import Producer
from utils.config import Config
from utils.file import File
from kafka.admin import KafkaAdminClient
# TODO test shoudld have setUP & tearDown but ignored for simplicity

class test_CorruptedMonitorFileValidation(unittest.TestCase):
    Config.set_env(Config.ENV_TEST)
    
    def test_b_corrupted_monitor_file(self):
        
        self.assertRaises(Exception, lambda: app.run(Config.K_MONITOR_TEST_TOPIC,
                                                    Config.PS_DATABASE_NAME,
                                                    Config.PS_TEST_WEBSITE_TABLE_NAME,
                                                    "tests/t_monitor_corrupted_interval.yml"))

    def test_a_corrupted_monitor_file(self):
        prod, cons = app.run(Config.K_MONITOR_TEST_TOPIC,
                            Config.PS_DATABASE_NAME,
                            Config.PS_TEST_WEBSITE_TABLE_NAME,
                            "tests/t_monitor_corrupted.yml")

        interval = File.read_time_interval("tests/t_monitor_corrupted.yml")

        time.sleep(interval-1)

        app.stop_monitor(prod, cons)

        print("Uncorrupted url= " + str(prod.get_message_count()))

        admin_client = KafkaAdminClient(bootstrap_servers=[Config.K_HOST+':'+Config.K_PORT],
                                security_protocol=Config.K_SECURITY_PROTOCOL,
                                ssl_cafile=Config.K_SSL_CAT_FILE,
                                ssl_certfile=Config.K_SSL_CERT_FILE,
                                ssl_keyfile=Config.K_SSL_KEY_FILE)

        admin_client.delete_topics([Config.K_MONITOR_TEST_TOPIC])

        self.assertEqual(prod.get_message_count(), cons.get_message_count())

if __name__ == '__main__': 
    unittest.main() 