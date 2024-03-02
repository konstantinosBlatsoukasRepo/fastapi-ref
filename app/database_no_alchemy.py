from psycopg2.extras import RealDictCursor
import psycopg2
import time

# connect to DB, without alchemy
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection succesfull!")
        break
    except Exception as error:
        print("Database connection failed")
        time.sleep(2)