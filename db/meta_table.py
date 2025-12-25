from db.db_connection import get_db_connection

def create_meta_tables():
    """
    create all meta schema tables.
    run once during db setup or migrations
    """
    create_sensor_table_sql = """
    CREATE TABLE IF NOT EXISTS meta.sensor (
    sensor_id SERIAL PRIMARY KEY,
    feeder_id INTEGER UNIQUE NOT NULL,
    feeder_name VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(create_sensor_table_sql)
            print("meta.sensor table created")
        conn.commit()
        print("Transaction committed")
    except Exception as e:
        print("ERROR", e)
    finally:
        conn.close()

if __name__ == "__main__":
    create_meta_tables()
    