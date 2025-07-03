import re
import mariadb
import time
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

app = Flask(__name__)

LOCKOUT_THRESHOLD = 5  # Number of allowed failed attempts
LOCKOUT_DURATION = 30 * 60  # 30 minutes in seconds

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

def is_account_locked(username):
    conn = mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
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

def record_failed_attempt(username):
    conn = mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            username VARCHAR(20) PRIMARY KEY,
            failed_attempts INT DEFAULT 0,
            lockout_time FLOAT DEFAULT 0
        )
    """)
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

def reset_failed_attempts(username):
    conn = mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            username VARCHAR(20) PRIMARY KEY,
            failed_attempts INT DEFAULT 0,
            lockout_time FLOAT DEFAULT 0
        )
    """)
    cursor.execute(
        "UPDATE login_attempts SET failed_attempts = 0, lockout_time = 0 WHERE username = %s",
        (username,)
    )
    conn.commit()
    conn.close()

def login(username, password):
    conn = mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"success": False, "error": "Missing username or password"}), 400

    username = sanitize_input(data['username'])
    password = sanitize_input(data['password'])

    if not validate_username(username):
        return jsonify({"success": False, "error": "Invalid username format"}), 400

    if not validate_password(password):
        return jsonify({"success": False, "error": "Invalid password format"}), 400

    if is_account_locked(username):
        return jsonify({"success": False, "error": "Account is locked. Try again later."}), 403

    if login(username, password):
        reset_failed_attempts(username)
        return jsonify({"success": True, "message": "Login successful!"}), 200
    else:
        record_failed_attempt(username)
        return jsonify({"success": False, "error": "Login failed. Check your credentials."}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)