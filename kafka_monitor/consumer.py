import threading
from db import Database
import json
from kafka import KafkaConsumer
from utils.config import Config
from datetime import datetime
from kafka.admin import KafkaAdminClient, NewTopic

class Consumer(threading.Thread):

    def __init__(self, topic: str, db: str, user: str, pw: str, host: str, port: str, table: str, is_test: bool):
        self.topic = topic
        self.db = db
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port
        self.table = table

        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.is_ready_event = threading.Event()

        # make thread dies with main thread in case of test env
        if is_test:
            threading.Thread.daemon = True

        self.consumer = KafkaConsumer(bootstrap_servers=[Config.K_HOST+':'+Config.K_PORT],
                                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                    security_protocol=Config.K_SECURITY_PROTOCOL,
                                    ssl_cafile=Config.K_SSL_CAT_FILE,
                                    ssl_certfile=Config.K_SSL_CERT_FILE,
                                    ssl_keyfile=Config.K_SSL_KEY_FILE)

        self.create_table_for_consumer()

        self.message_count = 0
    
    def is_ready(self):
        return self.is_ready_event.is_set()

    def stop(self):
        self.stop_event.set()

    def run(self):
        print("Consumer runs with topic \"" + self.topic + "\"!")

        # create topic if not exists
        if self.topic not in self.consumer.topics():
            self.create_monitor_topic()

        self.consumer.subscribe([self.topic])
        
        self.psql_conn = Database(self.db, self.user, self.pw, self.host, self.port)

        # consumer is ready to receive data 
        self.is_ready_event.set()
        
        while not self.stop_event.is_set():
            for message in self.consumer:
                self.message_count += 1
                print("\nConsumer receives " + message.value['name']+ " \n"+ str(message.value))
                self.insert_item_to_db(self.table, message.value)

                if self.stop_event.is_set():
                    break
        
        self.consumer.close()
        print("Consumer of \"" + self.topic + "\" is stopped!")

        if self.psql_conn:
            self.psql_conn.close()

                
                        
    def get_message_count(self) -> int:
        return self.message_count

    def create_table_for_consumer(self):
        psql_conn = Database(self.db, self.user, self.pw, self.host, self.port)
        psql_conn.query( """ CREATE TABLE IF NOT EXISTS """ + self.table + """ 
                        (name varchar(255),
                        website varchar(255) NOT NULL,
                        status_code integer NOT NULL,
                        reason varchar(255) NOT NULL,
                        response_time decimal NOT NULL,
                        checked_at timestamp NOT NULL,
                        pattern varchar(255),
                        has_pattern boolean DEFAULT FALSE,
                        PRIMARY KEY(website, checked_at))  """)

        psql_conn.close()

    def create_monitor_topic(self):
        print("Creating topic \"" + self.topic + "\" ... ")

        admin_client = KafkaAdminClient(bootstrap_servers=[Config.K_HOST+':'+Config.K_PORT],
                                security_protocol=Config.K_SECURITY_PROTOCOL,
                                ssl_cafile=Config.K_SSL_CAT_FILE,
                                ssl_certfile=Config.K_SSL_CERT_FILE,
                                ssl_keyfile=Config.K_SSL_KEY_FILE)

        website_topic  = [NewTopic(name=self.topic, num_partitions=Config.K_NO_PARTITIONS, 
                                    replication_factor=Config.K_REPLICA_FACTOR)]

        admin_client.create_topics(new_topics=website_topic)

    def insert_item_to_db(self, table: str, message: dict):

        if not self.psql_conn:
            print("Erorr Db not connected!")
            return

        query = "INSERT INTO " + table  + """ (name,
                                                website,
                                                status_code,
                                                reason,
                                                response_time,
                                                checked_at,
                                                pattern,
                                                has_pattern)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        vals = (message['name'],
                message['website'],
                message['status_code'],
                message['reason'],
                message['response_time'],
                datetime.now(),
                message['pattern'],
                message['has_pattern'])

        cursor = self.psql_conn.query(query, vals)

        if cursor.rowcount:
            print(str(cursor.rowcount) + " item inserted successfully in \"" + table + "\" table")