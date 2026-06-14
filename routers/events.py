from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime, timezone
import psycopg as ps
from config import config

router = APIRouter(prefix="/events", tags=["Events"])

# Helper function to get a database connection
def get_db_connection():
    params = config()
    return ps.connect(**params)

# Retrieves all events from the table
@router.get("/retrieve_all")
def get_events():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                crsr.execute("""
                             SELECT *
                             FROM event_table;
                             """)
                rows = crsr.fetchall()
                
                # Convert database tuples into JSON
                events = []
                for row in rows:
                    events.append({"event_id": row[0], 
                                  "event_name": row[1],
                                  "category": row[2],
                                  "average_time": row[3]
                                  })
                return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Creates an event in event_table
@router.post("/create")
def create_event(event_name: str, category: str):
    # makes everything lowercase for simplicity
    event_name = event_name.lower()
    category = category.lower()
    try:
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                
                # Check to see if event already exists
                crsr.execute("""
                             SELECT event_name FROM event_table
                             WHERE event_name = %s;
                             """, (event_name,))
                if crsr.fetchone():
                    raise HTTPException(status_code=409, detail="Event already exists.")
                
                # Insert event into database
                crsr.execute("""
                            INSERT INTO event_table (event_name, category)
                            VALUES (%s, %s);
                            """, (event_name, category))
                conn.commit()
                return {"message": f"{event_name} added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Deletes an event in event_table
@router.delete("/delete_event_name")
def delete_event(event_name: str):
    event_name = event_name.lower()
    try:
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                crsr.execute("""
                             DELETE FROM event_table
                             WHERE event_name = %s;
                             """, (event_name,))
                conn.commit()
                return {"message": f"{event_name} successfully deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))