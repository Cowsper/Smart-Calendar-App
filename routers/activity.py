# Used for debugging, remove in final product
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime, timezone, timedelta
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

@router.post("/average-start")
def calc_avg_start_time(event_name: str):
    # set event_name to lowercase
    event_name = event_name.lower()
    try:
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                # Retrieve event_id from event_name
                crsr.execute("""
                             SELECT event_id FROM event_table
                             WHERE event_name = %s;
                             """, (event_name,))
                row = crsr.fetchone()
                # raises error if event doesn't exist
                if not row:
                    raise HTTPException(status_code=404, detail="Event does not exist.")
                event_id = row[0]
                # gets all start and end times of every activity of the event selected
                crsr.execute("""
                            SELECT 
                                percentile_cont(0.5) WITHIN GROUP (ORDER BY (start_time::time)),
                                percentile_cont(0.5) WITHIN GROUP (ORDER BY (end_time::time)),
                                percentile_cont(0.5) WITHIN GROUP (ORDER BY (end_time - start_time)) 
                            FROM activity_table 
                            WHERE event_id = %s;
                            """, (event_id,))
                avg_start_time, avg_end_time, avg_duration = crsr.fetchone()
                if avg_start_time is None:
                    raise HTTPException(status_code=404, detail=f"No activities for {event_name}.")
                crsr.execute("""
                             UPDATE event_table
                             SET global_average_start_time = %s,
                                global_average_end_time = %s,
                                global_average_duration = %s
                             WHERE event_id = %s;
                             """, (avg_start_time, avg_end_time, avg_duration, event_id))
                conn.commit()
                return {"message": f"For {event_name}",
                        "global_average_start_time": str(avg_start_time),
                        "global_average_end_time": str(avg_end_time),
                        "average_duration": str(avg_duration)
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# @router.post("/average")
# def calc_avg_time(event_name: str):
#     # set event_name to lowercase
#     event_name = event_name.lower()
#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as crsr:
#                 # Retrieve event_id from event_name
#                 crsr.execute("""
#                              SELECT event_id FROM event_table
#                              WHERE event_name = %s;
#                              """, (event_name,))
#                 row = crsr.fetchone()
#                 # raises error if event doesn't exist
#                 if not row:
#                     raise HTTPException(status_code=404, detail="Event does not exist.")
#                 event_id = row[0]
#                 # gets all start and end times of every activity of the event selected
#                 crsr.execute("""
#                             SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY (end_time - start_time)) 
#                             FROM activity_table 
#                             WHERE event_id = %s;
#                             """, (event_id,))
#                 avg_time = crsr.fetchone()
#                 avg_time = avg_time[0]
#                 if avg_time is None:
#                     raise HTTPException(status_code=404, detail=f"No activities for {event_name}.")

                
#                 crsr.execute("""
#                              UPDATE event_table
#                              SET average_time = %s
#                              WHERE event_id = %s;
#                              """, (avg_time, event_id))
#                 conn.commit()
#                 return {"message": f"average time of {event_name} is {str(avg_time)}."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
                    
                