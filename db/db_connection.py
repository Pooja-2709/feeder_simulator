import psycopg

# DATABASE LAYER -> 
# create a postgreql connection 
# hides db credentials
# return a reusable connection


def get_db_connection():
    try:
        conn = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="dev1",
            user="postgres",
            password="P00ja@2709"
        )
        print("Database connected successfully")
        return conn 
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None