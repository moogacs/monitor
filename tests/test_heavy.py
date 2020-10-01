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
    Config.set_env(Config.ENV_TEST)
    
    #sorry https://aiven.io I made a lot of requests!

    def test_heavy(self):
        prod, cons = app.run(Config.K_MONITOR_TEST_TOPIC,
                            Config.PS_DATABASE_NAME,
                            Config.PS_TEST_WEBSITE_TABLE_NAME,
                            "tests/t_monitor_heavy_test.yml")

        time.sleep(30)

        app.stop_monitor(prod, cons)

        admin_client = KafkaAdminClient(bootstrap_servers=[Config.K_HOST+':'+Config.K_PORT],
                                        security_protocol=Config.K_SECURITY_PROTOCOL,
                                        ssl_cafile=Config.K_SSL_CAT_FILE,
                                        ssl_certfile=Config.K_SSL_CERT_FILE,
                                        ssl_keyfile=Config.K_SSL_KEY_FILE)

        admin_client.delete_topics([Config.K_MONITOR_TEST_TOPIC])

        self.assertEqual(prod.get_message_count(), cons.get_message_count())

if __name__ == '__main__': 
    unittest.main() 