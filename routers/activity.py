# Used for debugging, remove in final product
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime, timezone
import psycopg as ps
from config import config



router = APIRouter(prefix="/activites", tags=["Activities"])

# Helper function to get a database connection
def get_db_connection():
    params = config()
    return ps.connect(**params)

# Retrieves activities data from the table
@router.get("/")
def get_activities():
    try: 
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                crsr.execute("""
                             SELECT *
                             FROM activity_table;
                             """)
                rows = crsr.fetchall()
                activities = []
                for row in rows:
                    activities.append({
                        "user_id": row[0],
                        "event_id": row[1],
                        "start_time": row[2],
                        "end_time": row[3],
                        "activity_id": row[4]
                    })
                return activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
# Creates an activity in activity_table
@router.post("/")
def create_activity(user_id: int, event_id: int, start_time: datetime, end_time: datetime):
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="start_time must be before end_time.")   
    try:    
        with get_db_connection() as conn:
                with conn.cursor() as crsr:
                    
                    crsr.execute("""
                                INSERT INTO activity_table (user_id, event_id, start_time, end_time)
                                VALUES (%s, %s, %s, %s)
                                """, (user_id, event_id, start_time, end_time))
                    conn.commit()
                    return {"message": "Activity Successfully Registered!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Deletes an activity in activity_table
@router.delete("/")
def delete_activity(activity_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                crsr.execute("""
                             DELETE FROM activity_table
                             WHERE activity_id = %s;
                             """, (activity_id,))
                conn.commit()
                return {"message": f"{activity_id} successfully deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))