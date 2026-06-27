from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

@router.get("/lights")
def get_all_lights():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Dim_Light")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return {"count": len(rows), "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/readings")
def get_latest_readings():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 50 
                f.Reading_id,
                l.Li_id,
                l.Location,
                l.Status,
                f.Light_level,
                f.Motion_detection,
                d.FullDate,
                d.Hour
            FROM dbo.Fact_Sensor_Readings f
            JOIN dbo.Dim_Light l ON f.Li_id = l.Li_id
            JOIN dbo.Dim_Date d ON f.Date_id = d.Date_id
            ORDER BY f.Reading_id DESC
        """)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return {"count": len(rows), "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_stats():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_readings,
                AVG(Light_level) as avg_light_level,
                MAX(Light_level) as max_light_level,
                MIN(Light_level) as min_light_level
            FROM dbo.Fact_Sensor_Readings
        """)
        columns = [col[0] for col in cursor.description]
        row = dict(zip(columns, cursor.fetchone()))
        conn.close()
        return row
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))