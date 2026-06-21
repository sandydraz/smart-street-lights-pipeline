import asyncio
import json
import random
import pyodbc
from datetime import datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

# ── إعدادات Azure Event Hub ───────────────────────
CONNECTION_STR = "Endpoint=sb://slight-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=pKEWShjUOF8v7uWbFCiquYpm+3K204bdN+AEhLLQ+qQ="
EVENTHUB_NAME  = "sensor-readings"

# ── إعدادات SQL Server ────────────────────────────
SQL_CONN = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-35OUNGI\\SQLEXPRESS;"
    "DATABASE=SmartLightsDB;"
    "Trusted_Connection=yes;"
)

SENSOR_IDS = [f"SEN{i:04d}" for i in range(1, 101)]
LIGHT_IDS  = [f"SL{i:04d}"  for i in range(1, 51)]

def get_last_id():
    try:
        conn   = pyodbc.connect(SQL_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(R_id) FROM Sensor_readings")
        row = cursor.fetchone()[0]
        conn.close()
        if row:
            return int(row[2:]) + 1
        return 1
    except:
        return 1

counter = get_last_id()
print(f"هنبدأ من R_id: RD{counter:05d}")

def generate_reading():
    global counter
    sensor_id  = random.choice(SENSOR_IDS)
    sensor_num = int(sensor_id[3:])
    is_motion  = sensor_num % 2 == 1
    r_id       = f"RD{counter:05d}"
    counter   += 1

    return {
        "R_id":             r_id,
        "S_id":             sensor_id,
        "Li_id":            random.choice(LIGHT_IDS),
        "Timestamp":        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Motion_detection": random.choice([True, False]) if is_motion else None,
        "Light_level":      round(random.uniform(0, 100), 2) if not is_motion else None
    }

async def send_readings():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME
    )
    async with producer:
        print("Producer شغال — بيبعت reading كل 10 دقايق...")
        while True:
            batch   = await producer.create_batch()
            reading = generate_reading()
            batch.add(EventData(json.dumps(reading)))
            await producer.send_batch(batch)
            print(f"✅ اتبعت: {reading}")
            # await asyncio.sleep(5)   # كل 5 ثواني
            await asyncio.sleep(60)   # كل دقيقة

asyncio.run(send_readings())