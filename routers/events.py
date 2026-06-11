from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime, timezone
import psycopg as ps
from config import config

router = APIRouter(prefix="/events", tags=["Events"])

# Helper function to get a database connection
def get_db_connection():
    params = config()
    return ps.connect(**params)

# Retrieves events from the table
@router.get("/")
def get_events():
    pass

# Creates an event in event_table
@router.post("/")
def create_event():
    pass

# Deletes an event in event_table
@router.delete("/")
def delete_event():
    pass