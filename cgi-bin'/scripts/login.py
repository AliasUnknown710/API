#!/usr/bin/env python3

import cgi
import cgitb
import json
import sys
import os
import re
import mariadb
import time
from dotenv import load_dotenv

# Enable CGI error reporting
cgitb.enable()

# Load environment variables
load_dotenv()

# Print HTTP headers
print("Content-Type: application/json")
print("Access-Control-Allow-Origin: *")
print("Access-Control-Allow-Methods: POST, OPTIONS")
print("Access-Control-Allow-Headers: Content-Type")
print()  # Empty line required after headers

LOCKOUT_THRESHOLD = 5
LOCKOUT_DURATION = 30 * 60

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER") 
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def sanitize_input(user_input):
    return str(user_input).strip()

def validate_username(username):
    return re.fullmatch(r'^\w{3,20}$', username) is not None

def validate_password(password):
    return re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+=\-]{14,64}$', password) is not None

def get_db_connection():
    return mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def is_account_locked(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                username VARCHAR(20) PRIMARY KEY,
                failed_attempts INT DEFAULT 0,
                lockout_time FLOAT DEFAULT 0
            )
        """)
        cursor.execute("SELECT failed_attempts, lockout_time FROM login_attempts WHERE username = %s", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            failed_attempts, lockout_time = row
            if failed_attempts >= LOCKOUT_THRESHOLD:
                if time.time() < lockout_time + LOCKOUT_DURATION:
                    return True
        return False
    except Exception as e:
        print(json.dumps({"success": False, "error": "Database connection failed"}))
        sys.exit(1)

def record_failed_attempt(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT failed_attempts FROM login_attempts WHERE username = %s", (username,))
        row = cursor.fetchone()
        if row:
            failed_attempts = row[0] + 1
            lockout_time = time.time() if failed_attempts >= LOCKOUT_THRESHOLD else 0
            cursor.execute(
                "UPDATE login_attempts SET failed_attempts = %s, lockout_time = %s WHERE username = %s",
                (failed_attempts, lockout_time, username)
            )
        else:
            cursor.execute(
                "INSERT INTO login_attempts (username, failed_attempts, lockout_time) VALUES (%s, %s, %s)",
                (username, 1, 0)
            )
        conn.commit()
        conn.close()
    except Exception:
        pass

def reset_failed_attempts(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE login_attempts SET failed_attempts = 0, lockout_time = 0 WHERE username = %s",
            (username,)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

def login(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except Exception:
        return False

def main():
    # Handle preflight OPTIONS request
    if os.environ.get('REQUEST_METHOD') == 'OPTIONS':
        print(json.dumps({"success": True}))
        return
    
    # Only allow POST requests
    if os.environ.get('REQUEST_METHOD') != 'POST':
        print(json.dumps({"success": False, "error": "Method not allowed"}))
        return
    
    try:
        # Read POST data
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        if content_length == 0:
            print(json.dumps({"success": False, "error": "No data received"}))
            return
            
        post_data = sys.stdin.read(content_length)
        data = json.loads(post_data)
        
        if 'username' not in data or 'password' not in data:
            print(json.dumps({"success": False, "error": "Missing username or password"}))
            return

        username = sanitize_input(data['username'])
        password = sanitize_input(data['password'])

        if not validate_username(username):
            print(json.dumps({"success": False, "error": "Invalid username format"}))
            return

        if not validate_password(password):
            print(json.dumps({"success": False, "error": "Invalid password format"}))
            return

        if is_account_locked(username):
            print(json.dumps({"success": False, "error": "Account is locked. Try again later."}))
            return

        if login(username, password):
            reset_failed_attempts(username)
            print(json.dumps({"success": True, "message": "Login successful!"}))
        else:
            record_failed_attempt(username)
            print(json.dumps({"success": False, "error": "Login failed. Check your credentials."}))
            
    except json.JSONDecodeError:
        print(json.dumps({"success": False, "error": "Invalid JSON data"}))
    except Exception as e:
        print(json.dumps({"success": False, "error": "Internal server error"}))

if __name__ == "__main__":
    main()