from fastapi import FastAPI, HTTPException, APIRouter
from datetime import datetime, timezone, date
import psycopg as ps
from config import config
from security import is_password_valid, hash_password

router = APIRouter(prefix="/users", tags=["Users"])

# Function to get a database connection
def get_db_connection():
    params = config()
    return ps.connect(**params)

# Retrieves all users and every column in user_table
@router.get("/")
def get_users():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                crsr.execute("""
                             SELECT *
                             FROM user_table;
                             """)
                rows = crsr.fetchall()
                
                # Convert database tuples into JSON
                users = []
                for row in rows:
                    users.append({"user_id": row[0], 
                                  "password_hash": row[1],
                                  "first_name": row[2],
                                  "last_name": row[3],
                                  "email": row[4],
                                  "phone_number": row[5],
                                  "date_of_birth": row[6]
                                  })
                return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Creates a user in user_table
@router.post("/register")
def register_user(password: str, first_name: str, last_name: str, email: str, phone_number: str, date_of_birth: date):
    try:
        # Check Local Errors
        local_errors = []
        
        # Check if password is valid
        password_validity = is_password_valid(password)
        if password_validity[0] == False:
            local_errors.extend(password_validity[1])
        
        # Check if email is valid
        if "@" not in email:
            local_errors.append("Email is invalid")
            
        # Check the date isn't in the future
        today = date.today()
        if date_of_birth > today:
            local_errors.append(f"Date cannot be after {today}")
        
        # Check the date isn't before 1900
        if date_of_birth.year < 1900:
            local_errors.append(f"Date cannot be before 1900-01-01")
        
        if local_errors:
            raise HTTPException(status_code=400, detail=local_errors)  
        
        with get_db_connection() as conn:
            with conn.cursor() as crsr:
                
                # Database errors
                db_errors = []
                # Check if email is in database
                crsr.execute("""
                             SELECT email FROM user_table
                             WHERE email = %s;
                             """, (email,))
                if crsr.fetchone():
                    db_errors.append("Email Address already registered")
                # Check if phone number is in database
                crsr.execute("""
                             SELECT phone_number FROM user_table
                             WHERE phone_number = %s;
                             """, (phone_number,))
                if crsr.fetchone():
                    db_errors.append("Phone number already registered")
                
                if db_errors:
                    raise HTTPException(status_code=409, detail=db_errors)
                
                password_hash = hash_password(password)
                crsr.execute("""
                             INSERT INTO user_table (password_hash, first_name, last_name, email, phone_number, date_of_birth)
                             VALUES (%s, %s, %s, %s, %s, %s)
                             """, (password_hash, first_name, last_name, email, phone_number, date_of_birth))
                conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Deletes a user in user_table
@router.delete("/")
def delete_user():
    pass