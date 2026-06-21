"""
Smart Street Lights - Simulated Data Generator
Generates realistic CSV files based on the ERD diagram
"""

import csv
import random
import os
from datetime import datetime, timedelta

# ── Config ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = "smart_lights_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SEED = 42
random.seed(SEED)

# Simulation window: last 30 days
END_DATE   = datetime.now().replace(second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=30)

# Counts
NUM_LIGHTS      = 50
NUM_SENSORS     = NUM_LIGHTS * 2   # 2 sensors per light (motion + light-level)
NUM_ADMINS      = 5
NUM_TECHNICIANS = 10
NUM_COMMANDS    = 200
NUM_FAULTS      = 40
NUM_READINGS    = 5000   # sensor readings
NUM_TASKS       = 50     # maintenance tasks

# ── Helpers ─────────────────────────────────────────────────────────────────
EGYPTIAN_FIRST = [
    "Ahmed", "Mohamed", "Khaled", "Omar", "Ali", "Hassan", "Ibrahim",
    "Yousef", "Mahmoud", "Sami", "Sara", "Nour", "Dina", "Heba",
    "Rana", "Mariam", "Yasmine", "Layla", "Fatma", "Amira"
]
EGYPTIAN_LAST = [
    "Hassan", "Ibrahim", "Mostafa", "Saad", "Farouk", "Nasser",
    "Badr", "Saleh", "Khalil", "Mansour", "Amin", "Gaber",
    "Zaki", "Fouad", "Ragab", "Shawky", "Tawfik", "Wahba"
]
CAIRO_STREETS = [
    "Tahrir Square", "Nasr City", "Heliopolis", "Maadi", "Zamalek",
    "Dokki", "Mohandessin", "Giza", "6th of October", "New Cairo",
    "Shubra", "Ain Shams", "Abbassia", "Manial", "Agouza",
    "Imbaba", "Bolaq", "Sayeda Zeinab", "El Rehab", "Sheikh Zayed"
]

def rand_name():
    return f"{random.choice(EGYPTIAN_FIRST)} {random.choice(EGYPTIAN_LAST)}"

def rand_phone():
    prefix = random.choice(["010", "011", "012", "015"])
    return prefix + "".join([str(random.randint(0, 9)) for _ in range(8)])

def rand_email(name):
    parts = name.lower().split()
    return f"{parts[0]}.{parts[1]}{random.randint(1,99)}@smartlights.gov.eg"

def rand_datetime(start=START_DATE, end=END_DATE):
    delta = end - start
    secs  = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=secs)

def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def rand_coords():
    """Random coords roughly within Greater Cairo area"""
    lat = round(random.uniform(29.90, 30.20), 6)
    lon = round(random.uniform(31.10, 31.55), 6)
    return lat, lon

# ── 1. Admins ────────────────────────────────────────────────────────────────
print("Generating admins...")
admins = []
for i in range(1, NUM_ADMINS + 1):
    name = rand_name()
    admins.append({
        "A_id":  f"ADM{i:03d}",
        "Name":  name,
        "Phone": rand_phone(),
        "Email": rand_email(name)
    })

with open(f"{OUTPUT_DIR}/admins.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=admins[0].keys())
    w.writeheader(); w.writerows(admins)

# ── 2. Technicians ───────────────────────────────────────────────────────────
print("Generating technicians...")
technicians = []
specialties = ["Electrical", "Electronics", "Networking", "General Maintenance"]
for i in range(1, NUM_TECHNICIANS + 1):
    name = rand_name()
    technicians.append({
        "T_id":       f"TEC{i:03d}",
        "Name":       name,
        "Phone":      rand_phone(),
        "Specialty":  random.choice(specialties)
    })

with open(f"{OUTPUT_DIR}/technicians.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=technicians[0].keys())
    w.writeheader(); w.writerows(technicians)

# ── 3. Smart Lights (SLights) ────────────────────────────────────────────────
print("Generating smart lights...")
lights = []
statuses      = ["active", "inactive", "faulty", "maintenance"]
status_weights = [0.80, 0.05, 0.10, 0.05]

for i in range(1, NUM_LIGHTS + 1):
    lat, lon = rand_coords()
    street   = random.choice(CAIRO_STREETS)
    lights.append({
        "Light_id":         f"SL{i:04d}",
        "Location":         f"{street} ({lat}, {lon})",
        "Brightness_level": random.randint(0, 100),   # 0-100 %
        "Status":           random.choices(statuses, status_weights)[0],
        "Install_date":     fmt(rand_datetime(
                                START_DATE - timedelta(days=365*3),
                                START_DATE))
    })

with open(f"{OUTPUT_DIR}/slights.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=lights[0].keys())
    w.writeheader(); w.writerows(lights)

light_ids = [l["Light_id"] for l in lights]

# ── 4. Sensors ───────────────────────────────────────────────────────────────
print("Generating sensors...")
sensors = []
sensor_types = ["motion", "light_level"]

for i, light in enumerate(lights, 1):
    for stype in sensor_types:
        sid = f"SEN{len(sensors)+1:04d}"
        sensors.append({
            "S_id":     sid,
            "Type":     stype,
            "Light_id": light["Light_id"],
            "Status":   random.choices(["active", "faulty"], [0.92, 0.08])[0]
        })

with open(f"{OUTPUT_DIR}/sensors.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=sensors[0].keys())
    w.writeheader(); w.writerows(sensors)

sensor_ids = [s["S_id"] for s in sensors]

# ── 5. Sensor Readings ───────────────────────────────────────────────────────
print("Generating sensor readings...")

def realistic_light_level(dt: datetime) -> float:
    """Simulate realistic ambient light based on hour of day."""
    h = dt.hour
    if 6 <= h < 8:    return round(random.uniform(10, 40), 2)   # sunrise
    if 8 <= h < 17:   return round(random.uniform(60, 100), 2)  # daytime
    if 17 <= h < 20:  return round(random.uniform(10, 50), 2)   # sunset
    return round(random.uniform(0, 10), 2)                       # night

readings = []
for i in range(1, NUM_READINGS + 1):
    sensor = random.choice(sensors)
    ts     = rand_datetime()
    motion = random.choices([True, False], [0.25, 0.75])[0] \
             if sensor["Type"] == "motion" else None
    lv     = realistic_light_level(ts) \
             if sensor["Type"] == "light_level" else None

    readings.append({
        "Reading_id":       f"RD{i:05d}",
        "S_id":             sensor["S_id"],
        "Light_id":         sensor["Light_id"],
        "Timestamp":        fmt(ts),
        "Motion_detection": motion,
        "Light_level":      lv
    })

with open(f"{OUTPUT_DIR}/sensor_readings.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=readings[0].keys())
    w.writeheader(); w.writerows(readings)

# ── 6. Faults ────────────────────────────────────────────────────────────────
print("Generating faults...")
fault_types = [
    "Power failure", "Sensor malfunction", "Communication error",
    "Overheating", "Physical damage", "Flickering", "Dim output"
]
severities = ["low", "medium", "high", "critical"]
fault_weights = [0.30, 0.35, 0.25, 0.10]

faults = []
for i in range(1, NUM_FAULTS + 1):
    ts = rand_datetime()
    faults.append({
        "F_id":      f"FLT{i:04d}",
        "Light_id":  random.choice(light_ids),
        "F_type":    random.choice(fault_types),
        "Severity":  random.choices(severities, fault_weights)[0],
        "Timestamp": fmt(ts),
        "Resolved":  random.choices([True, False], [0.65, 0.35])[0]
    })

with open(f"{OUTPUT_DIR}/faults.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=faults[0].keys())
    w.writeheader(); w.writerows(faults)

fault_ids = [f["F_id"] for f in faults]

# ── 7. Commands ──────────────────────────────────────────────────────────────
print("Generating commands...")
command_types = [
    "turn_on", "turn_off", "set_brightness", "schedule_on",
    "schedule_off", "reset", "diagnostic_run", "firmware_update"
]

commands = []
for i in range(1, NUM_COMMANDS + 1):
    ts = rand_datetime()
    commands.append({
        "C_id":      f"CMD{i:04d}",
        "A_id":      random.choice(admins)["A_id"],
        "Light_id":  random.choice(light_ids),
        "C_type":    random.choice(command_types),
        "Timestamp": fmt(ts),
        "Status":    random.choices(
                         ["executed", "failed", "pending"],
                         [0.85, 0.10, 0.05])[0]
    })

with open(f"{OUTPUT_DIR}/commands.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=commands[0].keys())
    w.writeheader(); w.writerows(commands)

# ── 8. Maintenance Tasks ─────────────────────────────────────────────────────
print("Generating maintenance tasks...")
task_descriptions = [
    "Replace bulb", "Sensor calibration", "Wiring inspection",
    "Software update", "Physical cleaning", "Controller replacement",
    "Network module repair", "Full system check"
]
task_statuses = ["scheduled", "in_progress", "completed", "cancelled"]
task_weights  = [0.20, 0.15, 0.55, 0.10]

tasks = []
for i in range(1, NUM_TASKS + 1):
    start = rand_datetime()
    duration_hours = random.randint(1, 48)
    end   = start + timedelta(hours=duration_hours)
    tasks.append({
        "Task_id":     f"TSK{i:04d}",
        "T_id":        random.choice(technicians)["T_id"],
        "F_id":        random.choice(fault_ids) if random.random() < 0.7 else "",
        "Light_id":    random.choice(light_ids),
        "Description": random.choice(task_descriptions),
        "Start_date":  fmt(start),
        "End_date":    fmt(end),
        "Status":      random.choices(task_statuses, task_weights)[0]
    })

with open(f"{OUTPUT_DIR}/maintenance_tasks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=tasks[0].keys())
    w.writeheader(); w.writerows(tasks)

# ── Summary ──────────────────────────────────────────────────────────────────
print("\n✅ Data generation complete!")
print(f"{'Table':<22} {'Records':>8}  File")
print("-" * 55)
summary = [
    ("admins",            NUM_ADMINS,      "admins.csv"),
    ("technicians",       NUM_TECHNICIANS, "technicians.csv"),
    ("slights",           NUM_LIGHTS,      "slights.csv"),
    ("sensors",           NUM_SENSORS,     "sensors.csv"),
    ("sensor_readings",   NUM_READINGS,    "sensor_readings.csv"),
    ("faults",            NUM_FAULTS,      "faults.csv"),
    ("commands",          NUM_COMMANDS,    "commands.csv"),
    ("maintenance_tasks", NUM_TASKS,       "maintenance_tasks.csv"),
]
for name, count, fname in summary:
    print(f"  {name:<20} {count:>6}   {OUTPUT_DIR}/{fname}")