from fastapi import APIRouter, HTTPException
import subprocess
import sys
import os

router = APIRouter()

PRODUCER_PATH = r"C:\Users\RTXeg\Desktop\SLDB DATA\producer.py"
CONSUMER_PATH = r"C:\Users\RTXeg\Desktop\SLDB DATA\consumer.py"

producer_process = None
consumer_process = None

@router.post("/simulation/start")
def start_simulation():
    global producer_process, consumer_process

    if producer_process and producer_process.poll() is None:
        return {"status": "already_running", "message": "Simulation is already running"}

    try:
        consumer_process = subprocess.Popen(
            [sys.executable, CONSUMER_PATH],
            stdout=None,
            stderr=None,
            cwd=r"C:\Users\RTXeg\Desktop\SLDB DATA"
        )
        producer_process = subprocess.Popen(
            [sys.executable, PRODUCER_PATH],
            stdout=None,
            stderr=None,
             cwd=r"C:\Users\RTXeg\Desktop\SLDB DATA"
        )
        return {
            "status": "started",
            "message": "Producer and Consumer started successfully",
            "producer_pid": producer_process.pid,
            "consumer_pid": consumer_process.pid
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulation/stop")
def stop_simulation():
    global producer_process, consumer_process

    if not producer_process or producer_process.poll() is not None:
        return {"status": "not_running", "message": "Simulation is not running"}

    try:
        producer_process.terminate()
        consumer_process.terminate()
        producer_process = None
        consumer_process = None
        return {"status": "stopped", "message": "Producer and Consumer stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/simulation/status")
def simulation_status():
    global producer_process, consumer_process

    producer_running = producer_process is not None and producer_process.poll() is None
    consumer_running = consumer_process is not None and consumer_process.poll() is None

    return {
        "producer": "running" if producer_running else "stopped",
        "consumer": "running" if consumer_running else "stopped"
    }