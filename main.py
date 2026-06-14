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
app.include_router(events.router)
app.include_router(activity.router)

