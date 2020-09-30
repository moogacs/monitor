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

class test_heavy(unittest.TestCase):

    def test_heavy(self):
        prod, cons = app.run(Config.K_MONITOR_TEST_TOPIC,
                            Config.PS_DATABASE_NAME,
                            Config.PS_USERNAME,
                            Config.PS_PASSWORD,
                            Config.PS_HOST,
                            Config.PS_PORT,
                            Config.PS_TEST_WEBSITE_TABLE_NAME,
                            True,
                            "tests/t_monitor_heavy_test.yml")

        interval = File.read_time_interval("tests/t_monitor_heavy_test.yml")

        time.sleep(interval * 5)

        self.assertEqual(prod.get_message_count(), cons.get_message_count())

        app.stop_monitor(prod, cons)

        admin_client = KafkaAdminClient(bootstrap_servers=[Config.K_HOST+':'+Config.K_PORT],
                                        security_protocol=Config.K_SECURITY_PROTOCOL,
                                        ssl_cafile=Config.K_SSL_CAT_FILE,
                                        ssl_certfile=Config.K_SSL_CERT_FILE,
                                        ssl_keyfile=Config.K_SSL_KEY_FILE)

        admin_client.delete_topics([Config.K_MONITOR_TEST_TOPIC])

        

if __name__ == '__main__': 
    unittest.main() 