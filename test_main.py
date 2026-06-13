from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import psycopg as ps
from config import config
from routers import users, events, activity
import json

app = FastAPI(title="Smart Calendar API")

# Function to get a database connection
def get_db_connection():
    params = config()
    return ps.connect(**params)

app.include_router(users.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}



# --- ENDPOINT 2: Log a New Activity ---
@app.post("/activities")
def create_activity(user_id: int, event_id: int, start_time: datetime, end_time: datetime):
    # Quick validation before wasting database resources
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
        
    try:
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                crsr.execute("""
                    INSERT INTO activity_table (user_id, event_id, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                    RETURNING activity_id;
                """, (user_id, event_id, start_time, end_time))
                
                conn.commit()
                
                return {"message": "Activity logged successfully"}
                
    except ps.errors.CheckViolation:
        raise HTTPException(status_code=400, detail="Database rejected times: end_time must be after start_time")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))