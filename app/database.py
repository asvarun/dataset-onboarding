import time
import psycopg2
from psycopg2.extras import RealDictCursor


# Check with repo owner for DB Credentials
def database():
    while True:
        try:
            conn = psycopg2.connect(host='localhost', dbname='nike', user='', password='',
                                    cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database connection was successful!")
            return conn, cursor

        except Exception as error:
            print("Connection to database failed")
            print("Error:", error)
            print("Type of Error", type(error))
            time.sleep(2)
