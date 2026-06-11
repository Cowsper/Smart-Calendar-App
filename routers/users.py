from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime, timezone
import psycopg as ps
from config import config

router = APIRouter(prefix="/users", tags=["Users"])

# Helper function to get a database connection
def get_db_connection():
    params = config()
    return ps.connect(**params)

# Retrieves user data or users from the table
@router.get("/")
def get_users():
    pass

# Creates a user in user_table
@router.post("/")
def create_user():
    pass

# Deletes a user in user_table
@router.delete("/")
def delete_user():
    pass