import asyncio
import json
import pyodbc
from azure.eventhub.aio import EventHubConsumerClient

# ── إعدادات Azure Event Hub ───────────────────────
CONNECTION_STR  = "Endpoint=sb://slight-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=pKEWShjUOF8v7uWbFCiquYpm+3K204bdN+AEhLLQ+qQ="
EVENTHUB_NAME   = "sensor-readings"
CONSUMER_GROUP  = "$Default"

# ── إعدادات SQL Server ────────────────────────────
SQL_CONN = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-35OUNGI\\SQLEXPRESS;"
    "DATABASE=SmartLightsDB;"
    "Trusted_Connection=yes;"
)

def save_to_db(reading):
    try:
        conn   = pyodbc.connect(SQL_CONN)
        cursor = conn.cursor()

        # لو مفيش R_id في الـ message القديمة، تجاهليها
        if "R_id" not in reading:
            print(f"⚠️ Message قديمة بدون R_id — متتجاهلتش")
            conn.close()
            return

        motion = None
        if reading["Motion_detection"] is not None:
            motion = 1 if reading["Motion_detection"] else 0

        cursor.execute("""
            INSERT INTO Sensor_readings
                (R_id, S_id, Li_id, Timestamp, Motion_detection, Light_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            reading["R_id"],
            reading["S_id"],
            reading["Li_id"],
            reading["Timestamp"],
            motion,
            reading["Light_level"]
        )
        conn.commit()
        conn.close()
        print(f"✅ اتحفظت: {reading['R_id']} - {reading['S_id']}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def on_event(partition_context, event):
    reading = json.loads(event.body_as_str())
    save_to_db(reading)
    await partition_context.update_checkpoint(event)

async def receive():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME
    )
    async with client:
        print("Consumer شغال — بيستنى readings...")
        await client.receive(
            on_event=on_event,
            starting_position="@latest"
        )

asyncio.run(receive())