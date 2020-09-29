import unittest 
import sys
import os
import time
import app
from db import Database

from kafka_monitor.consumer import Consumer
from kafka_monitor.producer import Producer
from utils.config import Config
from utils.file import File

# TODO test shoudld have setUP & tearDown but ignored for simplicity

class DB(unittest.TestCase):

    def test_db(self):

        aiven_results = 0

        psql_conn = Database(Config.PS_DATABASE_NAME, Config.PS_USERNAME, Config.PS_PASSWORD, Config.PS_HOST, Config.PS_PORT)
        
        print("DB \"" + Config.PS_DATABASE_NAME + "\" is Connected!")

        query =  """ CREATE TABLE IF NOT EXISTS """ + Config.PS_TEST_WEBSITE_TABLE_NAME  + """ (
                    name varchar(255) NOT NULL,
                    website varchar(255) NOT NULL,
                    status_code integer NOT NULL,
                    reason varchar(255) NOT NULL,
                    response_time decimal NOT NULL,
                    checked_at timestamp NOT NULL,
                    pattern varchar(255),
                    has_pattern boolean DEFAULT FALSE,
                    PRIMARY KEY(website, checked_at)
                )  """
                
        psql_conn.query(query)
        
        query = "DELETE FROM " + Config.PS_TEST_WEBSITE_TABLE_NAME +  " WHERE website = 'https://aiven.io'"
        psql_conn.query(query)
        
        prod, cons = app.run(Config.K_MONITOR_TOPIC,
                            Config.PS_DATABASE_NAME,
                            Config.PS_USERNAME,
                            Config.PS_PASSWORD,
                            Config.PS_HOST,
                            Config.PS_PORT,
                            Config.PS_TEST_WEBSITE_TABLE_NAME,
                            True,
                            "tests/t_monitor_db.yml")

        interval = File.read_time_interval("tests/t_monitor_db.yml")

        time.sleep(interval//2)

        app.stop_monitor(prod, cons)
        
        query = "SELECT * FROM " + Config.PS_TEST_WEBSITE_TABLE_NAME +  " WHERE website = 'https://aiven.io'"
        cursor = psql_conn.query(query)
        aiven_results = cursor.fetchall()

        psql_conn.close()
        print("\"" + Config.PS_TEST_WEBSITE_TABLE_NAME + "\" table created successfully in PostgreSQL ")

        self.assertEqual(len(aiven_results), 1)

if __name__ == '__main__':
    unittest.main() 