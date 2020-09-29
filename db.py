import psycopg2
from utils.config import Config
from datetime import datetime

class Database():
    def __init__(self, db, user, password, host, port):
        try:
            self.conn = psycopg2.connect( database = db,
                                            user = user,
                                            password = password,
                                            host = host,
                                            port = port)
            self.cursor = self.conn.cursor()
            self.db = db

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)

    def query(self, query: str, vars=None) -> psycopg2.extensions.cursor:
        try:
            if vars:
                self.cursor.execute(query, vars)
            else:
                self.cursor.execute(query)

            self.conn.commit()

            return self.cursor
        except (Exception, psycopg2.Error) as error :
            print ("Error while querying PostgreSQL", error)
            return self.cursor

    # close communication with the PostgreSQL database server
    def close(self )-> bool: 
        try: 
            self.cursor.close()
            self.conn.close()
            print ("\"" + self.db + "\" DB is disconnected!")
            return True

        except (Exception, psycopg2.Error) as error :
            print ("Error while querying PostgreSQL", error)
            return False