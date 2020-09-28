import threading
from db import Database
import json
from kafka import KafkaConsumer
from config import Config
from datetime import datetime

class Consumer(threading.Thread):
    message_count = 0
    
    def __init__(self, topic: str, db: str, user: str, pw: str, host: str, port: str, table: str):        
        self.topic = topic
        self.db = db
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port
        self.table = table

        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        psql_conn = Database(self.db, self.user, self.pw, self.host, self.port)
        psql_conn.query( """ CREATE TABLE IF NOT EXISTS """ + self.table + """ 
                        (name varchar(255) NOT NULL,
                        website varchar(255) NOT NULL,
                        status_code integer NOT NULL,
                        reason varchar(255) NOT NULL,
                        response_time decimal NOT NULL,
                        checked_at timestamp NOT NULL,
                        pattern varchar(255),
                        has_pattern boolean DEFAULT FALSE,
                        PRIMARY KEY(website, checked_at))  """)

        psql_conn.close()

        Consumer.message_count = 0
        self.stop_event = threading.Event()

    def stop(self):
        self.consumer.close()
        print("Consumer stopped!")
        self.stop_event.set()

    def run(self):
        print("Consumer runs!")
        self.consumer = KafkaConsumer(bootstrap_servers=[Config.K_HOST+':'+Config.K_PORT],
                                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                    security_protocol=Config.K_SECURITY_PROTOCOL,
                                    ssl_cafile=Config.K_SSL_CAT_FILE,
                                    ssl_certfile=Config.K_SSL_CERT_FILE,
                                    ssl_keyfile=Config.K_SSL_KEY_FILE)

        self.consumer.subscribe([self.topic])

        psql_conn = Database(self.db, self.user, self.pw, self.host, self.port)

        while not self.stop_event.is_set():
            for message in self.consumer:
                Consumer.message_count += 1
                print("\nConsumer receive " + message.value['name']+ " \n"+ str(message.value))

                query = "INSERT INTO " + self.table  + """ (name,
                                                            website,
                                                            status_code,
                                                            reason,
                                                            response_time,
                                                            checked_at,
                                                            pattern,
                                                            has_pattern)
                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

                vals = (message.value['name'],
                        message.value['website'],
                        message.value['status_code'],
                        message.value['reason'],
                        message.value['response_time'],
                        datetime.now(),
                        message.value['pattern'],
                        message.value['has_pattern'])

                success = psql_conn.query(query, vals)
                if success:
                    print("item inserted successfully in PostgreSQL")

                if self.stop_event.is_set():
                    psql_conn.close()
                    break
                        
    def get_message_count() -> int:
        return Consumer.message_count