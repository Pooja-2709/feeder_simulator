# BUSINESS LOGIC LAYER -> 
# parses request data
# validate input
# applies rules(like unique sensor, required fields)
# call db layer
# """create a sensor in meta.sensor"""
import json
from db.db_connection import get_db_connection

insert_sensor_sql = """
    Insert into meta.sensor(feeder_id, feeder_name)
    values (%s, %s)
    ON CONFLICT (feeder_id) DO NOTHING;
    """

check_sensor_sql = """
select 1 from meta.sensor where feeder_id=%s;
"""

def create_sensor(request_body):
    try:
        data = json.loads(request_body)

        feeder_id = data.get("feeder_id")
        feeder_name = data.get("feeder_name")

        if feeder_id is None or feeder_name is None:
            return 400, {"error": "feeder_id and feeder_name are required"}
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # check duplicates
                cur.execute(
                    check_sensor_sql, (feeder_id,)
                )
                if cur.fetchone():
                    return 409, {"error": "sensor with feeder_id already exists"}
                
                cur.execute(insert_sensor_sql, (feeder_id, feeder_name))
                conn.commit()
            
            return 201, {"message": "Sensor created successfully"}
        finally:
            conn.close()

    except json.JSONDecodeError:
        return 400, {"error": "Invalid json format"}
    
    except Exception as e:
        return 500, {"error": str(e)}
    