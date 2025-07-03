import re
import mariadb
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

app = Flask(__name__)

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

def user_exists(username):
    conn = mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(20) PRIMARY KEY,
            password VARCHAR(128) NOT NULL
        )
    """)
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def create_user(username, password):
    conn = mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(20) PRIMARY KEY,
            password VARCHAR(128) NOT NULL
        )
    """)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()

@app.route('/signup', methods=['POST'])
def signup_route():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"success": False, "error": "Missing username or password"}), 400

    username = sanitize_input(data['username'])
    password = sanitize_input(data['password'])

    if not validate_username(username):
        return jsonify({"success": False, "error": "Invalid username format"}), 400

    if not validate_password(password):
        return jsonify({"success": False, "error": "Invalid password format"}), 400

    if user_exists(username):
        return jsonify({"success": False, "error": "Username already exists"}), 409

    create_user(username, password)
    return jsonify({"success": True, "message": "Signup successful!"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)