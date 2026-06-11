import psycopg as ps
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
        
        # Create user_table table
        crsr.execute("""
                    CREATE TABLE IF NOT EXISTS user_table (
                        user_id SERIAL PRIMARY KEY NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        first_name VARCHAR(255) NOT NULL,
                        last_name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        phone_number VARCHAR(50) NOT NULL,
                        date_of_birth DATE NOT NULL
                    );
                    """)
        
        connection.commit()
        print("User Table Added (If doesn't exist)")
        
        # Create event_table table
        crsr.execute("""
                    CREATE TABLE IF NOT EXISTS event_table (
                        event_id SERIAL PRIMARY KEY NOT NULL,
                        event_name VARCHAR(255) NOT NULL,
                        category VARCHAR(255) NOT NULL,
                        average_time INTERVAL
                    );
                    """)
        
        connection.commit()
        print("Event Table Added (If doesn't exist)")
        
        # Create activity_table table
        crsr.execute("""
                    CREATE TABLE IF NOT EXISTS activity_table (
                        user_id INTEGER REFERENCES user_table(user_id) NOT NULL,
                        event_id INTEGER REFERENCES event_table(event_id) NOT NULL,
                        start_time TIMESTAMPTZ NOT NULL,
                        end_time TIMESTAMPTZ NOT NULL,
                        
                        CONSTRAINT time_validity_check CHECK (end_time > start_time)
                    );
                    """)
        
        connection.commit()
        print("Activity Table Added (If doesn't exist)")        
        crsr.close()
    except(Exception, ps.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("DB connection terminated.")
if __name__ == "__main__":
    connect()