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
    pass

# Creates an activity in activity_table
@router.post("/")
def create_activity():
    pass

# Deletes an activity in activity_table
@router.delete("/")
def delete_activity():
    pass