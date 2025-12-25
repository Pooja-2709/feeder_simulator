import time 
import random
import uuid

from db.db_connection import get_db_connection

fetch_sensor_sql = """
select feeder_id 
from meta.sensor
where is_active=true;
"""
# print(fetch_sensor_sql)
insert_raw_data_sql ="""
insert into raw.sensordata(id, feeder_id, eventtime, energy_raw_value)
values(%s,%s,%s,%s);
"""

class FeederDataGenerator:
    """
    Long-running generator that produces energy data
    for each active feeder every minute.
    """
    def __init__(self):
        self.energy_state = {}
        print(f"Energy state map: {self.energy_state}")

    def fetch_active_feeder(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(fetch_sensor_sql)
                return [row[0] for row in cur.fetchall()]
        finally:
            conn.close()

    def generate_raw_value(self, feeder_id):
        base = self.energy_state.get(feeder_id, random.uniform(10, 50))
        increment = random.uniform(0.5, 2.5)
        new_value = base + increment
        self.energy_state[feeder_id] = new_value
        return round(new_value, 3)

    def generate_eventtime_epoch(self):
        return int(time.time())

    def run(self):
        print("Feeder data generator started")

        while True:
            feeders = self.fetch_active_feeder()
            if not feeders:
                print("No active feeders found")
                time.sleep(60)
                continue

            conn = get_db_connection()
            try:
                with conn.cursor() as cur:
                    for feeder_id in feeders:
                        energy = self.generate_raw_value(feeder_id)
                        eventtime = self.generate_eventtime_epoch()
                        cur.execute(
                            insert_raw_data_sql,
                            (
                                str(uuid.uuid4()),
                                feeder_id, 
                                eventtime,
                                energy
                            )
                        )
                        
                        print(
                            f"feeder_id={feeder_id} |"
                            f"energy_raw={energy} |"
                            f"eventtime={eventtime}"
                        )
                conn.commit()
                print(f"Generated data for {len(feeders)} feeders")

            except Exception as e:
                print(f"Error generating data {e}")

            finally:
                conn.close()

            time.sleep(60)

if __name__=="__main__":
    FeederDataGenerator().run()
    # breakpoint()