# 🚦 Smart Street Lights — Full System

An end-to-end data engineering pipeline that simulates IoT sensor data from smart street lights, streams it through Azure Event Hub,
stages it in SQL Server, loads it incrementally into a Data Warehouse (Galaxy Schema) using SSIS — and exposes it via a FastAPI backend with a live dashboard.

> Event Hub acts as a **temporary buffer** between the Producer and Consumer — it is **not** a final data store.

---

## △ Architecture

![Smart Street Lights — Full System Architecture](docs/architecture.png)

> FastAPI backend added on top of the existing pipeline — exposes REST endpoints and serves a live dashboard.

— — — Streaming (temporary buffer) ─── Persistent storage / ETL flow

| Stage | Component | Role |
|-------|-----------|------|
| 1 | Python Producer | Generates simulated sensor data and sends it as events |
| 2 | Azure Event Hub | Temporary streaming buffer (not persistent storage) |
| 3 | Python Consumer | Reads events from Event Hub and inserts raw records into staging |
| 4 | SQL Server (Staging) | Stores raw, unprocessed sensor records |
| 5 | SSIS Pipeline | Performs incremental load — moves only new records |
| 6 | Data Warehouse (Galaxy Schema) | Final destination — Fact + Dimension tables for analytics |
| 7 | FastAPI Backend | Reads from SmartLightsDW — exposes REST endpoints + controls simulation |
| 8 | Live Dashboard | Browser-based HTML/JS dashboard with Chart.js and auto-refresh |

---

## ✶ Tech Stack

- **Python** — data simulation (Producer) & event consumption (Consumer)
- **Azure Event Hub** ( `Slight-eventhub` ) — real-time event streaming
- **SQL Server** — staging database & data warehouse
- **SSIS (SQL Server Integration Services)** — ETL / incremental load
- **FastAPI** — REST API backend (`smart_streetlights_api`)
- **HTML / JavaScript / Chart.js** — live dashboard with auto-refresh polling
- **draw.io** — architecture diagram

---

## ⌂ Project Structure

```
smart-street-lights-pipeline/
│
├── smart_lights_data/
│   ├── producer.py          # Generates & sends simulated sensor data to Event Hub
│   ├── consumer.py          # Reads events from Event Hub, inserts into staging DB
│   └── generated_data.py    # Simulated sensor data generation logic
│
├── sql/
│   ├── SmartLightsDB.sql    # Staging database schema (SmartLightsDB)
│   └── SmartLightsDW.sql    # Data Warehouse schema (SmartLightsDW - Fact + Dimension tables)
│
├── ssis/
│   ├── Load_DB.dtsx         # SSIS package - loads raw events into staging (SmartLightsDB)
│   └── Load_DW.dtsx         # SSIS package - incremental load into warehouse (SmartLightsDW)
│
├── api/
│   ├── main.py              # FastAPI app entry point — CORS, router registration
│   ├── database.py          # pyodbc connection to SmartLightsDW (Windows Auth)
│   └── routers/
│       ├── lights.py        # GET /api/lights — list all lights from Dim_Light
│       ├── readings.py      # GET /api/readings — latest sensor readings from Fact_Sensor_Readings
│       ├── stats.py         # GET /api/stats — aggregated stats (avg brightness, motion %, etc.)
│       └── simulation.py    # POST /api/simulation/start|stop — subprocess control
│
├── dashboard/
│   └── dashboard.html       # Live HTML dashboard — Chart.js + auto-refresh polling
│
├── docs/
│   └── architecture.png     # Architecture diagram
│
├── .env.example             # Environment variable template
└── README.md
```

---

## ⚙ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/sandydraz/smart-street-lights-pipeline.git
cd smart-street-lights-pipeline
```

### 2. Configure environment variables

Create a `.env` file based on `.env.example`, using your Slight-eventhub connection details:

```env
EVENT_HUB_CONNECTION_STR=<your-event-hub-connection-string>
EVENT_HUB_NAME=Slight-eventhub
SQL_SERVER=<your-sql-server-address>
SQL_DATABASE=SmartLightsDB
```

> **Note:** The FastAPI backend connects to `SmartLightsDW` using **Windows Authentication** (no username/password required).

### 3. Set up the SQL Server staging database

Run the schema script in SQL Server Management Studio (SSMS):

```
sql/SmartLightsDB.sql
```

### 4. Set up the Data Warehouse

```
sql/SmartLightsDW.sql
```

---

## ▶ Running the Pipeline

**Step 1 — Generate simulated data:**

```bash
python smart_lights_data/generated_data.py
```

**Step 2 — Start the Producer** (sends simulated data to Event Hub):

```bash
python smart_lights_data/producer.py
```

**Step 3 — Start the Consumer** (reads from Event Hub, writes to staging):

```bash
python smart_lights_data/consumer.py
```

**Step 4 — Run the SSIS packages** to load data into the warehouse:

- Open `ssis/Load_DB.dtsx` in Visual Studio (SSDT) — loads/validates raw records into SmartLightsDB staging
- Open `ssis/Load_DW.dtsx` — performs the incremental load into SmartLightsDW
- Execute manually, or schedule via SQL Server Agent for automated runs

**Step 5 — Start the FastAPI backend:**

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`
Interactive docs (Swagger UI): `http://localhost:8000/docs`

**Step 6 — Open the Live Dashboard:**

Open `dashboard/dashboard.html` in your browser. The dashboard auto-refreshes every few seconds by polling the FastAPI backend.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/lights` | List all street lights from `Dim_Light` |
| GET | `/api/readings` | Latest sensor readings from `Fact_Sensor_Readings` |
| GET | `/api/stats` | Aggregated stats — avg brightness, motion detection %, energy usage |
| POST | `/api/simulation/start` | Start the IoT producer subprocess |
| POST | `/api/simulation/stop` | Stop the IoT producer subprocess |

> All endpoints read from `SmartLightsDW` via Windows Authentication (pyodbc trusted connection).

---

## 📊 Live Dashboard

The dashboard (`dashboard/dashboard.html`) connects to the FastAPI backend via `HTTP fetch()` and displays:

- **Real-time sensor readings** — brightness levels, motion detection status
- **Charts** — light level trends over time (Chart.js)
- **Simulation controls** — Start / Stop buttons that trigger the producer via the API
- **Auto-refresh** — polls the backend every few seconds without manual reload

---

## ➤ Data Flow Summary

```
Python Producer
  → Azure Event Hub (Slight-eventhub)
    → Python Consumer
      → SmartLightsDB (Staging)
        → SSIS (Load_DB → Load_DW)
          → SmartLightsDW (Galaxy Schema)
            → FastAPI Backend
              → Live Dashboard (Browser)
```

1. The **Producer** simulates sensor readings (light status, brightness, motion detection, energy usage) and pushes them as events to `Slight-eventhub`.
2. **Event Hub** temporarily buffers these events for consumption.
3. The **Consumer** reads the events and inserts raw rows into the `SmartLightsDB` staging database.
4. **Load_DB.dtsx** validates/stages the records, then **Load_DW.dtsx** performs an incremental load — only new records since the last run — into `SmartLightsDW`.
5. The **Data Warehouse** organizes data into Fact and Dimension tables (Galaxy Schema), ready for reporting and analysis.
6. The **FastAPI backend** queries `SmartLightsDW` directly using Windows Authentication and exposes REST endpoints for lights, readings, stats, and simulation control.
7. The **Live Dashboard** polls the FastAPI backend every few seconds and renders up-to-date charts and sensor data in the browser.

---

## 📝 Notes

- The staging database (`SmartLightsDB`) holds raw, unprocessed data — intentionally separate from the warehouse to keep ingestion and analytics layers decoupled.
- The SSIS pipeline uses an **incremental load** strategy, so only newly inserted records are processed on each run, avoiding duplicates.
- The FastAPI backend uses **Windows Authentication** (trusted connection) — no SQL username/password needed.
- The 3-tier architecture (Dashboard → FastAPI → Data Warehouse) keeps the presentation layer decoupled from the data layer, allowing the dashboard to be hosted or shared independently.
- This project is for educational purposes as part of a data engineering coursework/portfolio project.
