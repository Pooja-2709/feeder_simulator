from db.db_connection import get_db_connection

def create_raw_tables():
    """
    create raw schema tables.
    """
    create_raw_sensor_table_sql = """
    CREATE TABLE IF NOT EXISTS raw.sensordata (
        id UUID PRIMARY KEY,
        feeder_id INTEGER NOT NULL,
        timestamp_utc TIMESTAMPTZ NOT NULL,
        energy_raw_value NUMERIC(12,4) NOT NULL
    );
    """
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(create_raw_sensor_table_sql)
            print("raw.sensordata table created")
        conn.commit()
        print("transaction committed")
    except Exception as e:
        print("error", e)
    finally:
        conn.close()

if __name__ == "__main__":
    create_raw_tables()
