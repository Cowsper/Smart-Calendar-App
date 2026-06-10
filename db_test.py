import psycopg2 as ps
from config import config

def connect():
    connection = None
    try:
        params = config()
        print('Connection to postgreSQL database')
        connection = ps.connect(**params)
        
        # create cursor
        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute("SELECT version()")
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()
    except(Exception, ps.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("DB connection terminated.")
if __name__ == "__main__":
    connect()