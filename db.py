import psycopg2
from config import Config 
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
            return True

        except (Exception, psycopg2.Error) as error :
            print ("Error while querying PostgreSQL", error)
            return False

        
# def ps_create_table():
#     connection = None
#     try:
#         connection = psycopg2.connect( database = Config.PS_DATABASE_NAME,
#                                         user = Config.PS_USERNAME,
#                                         password = Config.PS_PASSWORD,
#                                         host = Config.PS_HOST,
#                                         port = Config.PS_PORT)
#         print("DB Connected!")
#         cursor = connection.cursor()
#         query = """ CREATE TABLE IF NOT EXISTS """ + Config.PS_WEBSITE_TABLE_NAME + """ (
#                     name varchar(255) NOT NULL,
#                     website varchar(255) NOT NULL,
#                     status_code integer NOT NULL,
#                     reason varchar(255) NOT NULL,
#                     response_time decimal NOT NULL,
#                     checked_at timestamp NOT NULL,
#                     pattern varchar(255),
#                     has_pattern boolean DEFAULT FALSE,
#                     PRIMARY KEY(website, checked_at)
#                 )  """

#         cursor.execute(query)

#         # close communication with the PostgreSQL database server
#         cursor.close()

#         # commit the changes
#         connection.commit()
#         print("Table created successfully in PostgreSQL ")


#     except (Exception, psycopg2.DatabaseError) as error :
#         print ("Error while connecting to PostgreSQL", error)
#     finally:
#         if connection is not None:
#             connection.close()

# def ps_insert_item(website_status):
#     connection = None
#     try:
#         connection = psycopg2.connect( database = Config.PS_DATABASE_NAME,
#                                         user = Config.PS_USERNAME,
#                                         password = Config.PS_PASSWORD,
#                                         host = Config.PS_HOST, 
#                                         port = Config.PS_PORT)
#         print("DB Connected!")

#         cursor = connection.cursor()

#         query = "INSERT INTO " + Config.PS_WEBSITE_TABLE_NAME  + " (name, website, status_code, reason, response_time, checked_at, pattern, has_pattern) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

#         cursor.execute(query,(website_status['name'],
#                             website_status['website'],
#                             website_status['status_code'],
#                             website_status['reason'],
#                             website_status['response_time'],
#                             datetime.now(),
#                             website_status['pattern'],
#                             website_status['has_pattern']))

#         # close communication with the PostgreSQL database server
#         cursor.close()

#         # commit the changes
#         connection.commit()
#         print("item inserted successfully in PostgreSQL ")


#     except (Exception, psycopg2.DatabaseError) as error :
#         print ("Error while connecting to PostgreSQL", error)
#     finally:
#         if connection is not None:
#             connection.close()