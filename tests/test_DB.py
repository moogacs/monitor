import unittest 
import sys
import os
import time
sys.path.append("..")
import app
from db import Database

from config import Config 
from kafka_client.Consumer import Consumer
from kafka_client.Producer import Producer

class DB(unittest.TestCase):

    def test_db(self):
        connection = None
        aiven_results = 0
        try: 
            
            psql_conn = Database(Config.PS_DATABASE_NAME, Config.PS_USERNAME, Config.PS_PASSWORD, Config.PS_HOST, Config.PS_PORT)
            
            print("DB Connected!")

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
            time.sleep(5)
            app.stop_monitor(prod, cons)
            
            query = "SELECT * FROM " + Config.PS_TEST_WEBSITE_TABLE_NAME +  " WHERE website = 'https://aiven.io'"
            cursor = psql_conn.query(query)
            aiven_results = cursor.fetchall()

            psql_conn.close()
            print("Table created successfully in PostgreSQL ")


        except Exception as error :
            print ("Error while connecting to PostgreSQL", error)

        self.assertEqual(len(aiven_results), 1)

if __name__ == '__main__':
    unittest.main() 