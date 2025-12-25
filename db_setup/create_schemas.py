from db.db_connection import get_db_connection

create_schema_sql = """
          create schema if not exists meta;
          create schema if not exists raw;
          """

def create_schemas():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(create_schema_sql)
        print("Schemas 'meta' and 'raw' created successfully")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_schemas()