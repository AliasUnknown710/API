#!/usr/bin/env python3

import cgi
import cgitb
import json
import sys
import os
import mariadb
from dotenv import load_dotenv

# Enable CGI error reporting
cgitb.enable()

# Load environment variables
load_dotenv()

# Print HTTP headers
print("Content-Type: application/json")
print("Access-Control-Allow-Origin: *")
print("Access-Control-Allow-Methods: DELETE, OPTIONS")
print("Access-Control-Allow-Headers: Content-Type, Authorization")
print()  # Empty line required after headers

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_db_connection():
    return mariadb.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def delete_profile_from_db(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        return deleted_count > 0
    except Exception as e:
        return False

def validate_auth_token(auth_token):
    # Add your token validation logic here
    # For now, just check if token exists
    return auth_token and len(auth_token) > 0

def main():
    # Handle preflight OPTIONS request
    if os.environ.get('REQUEST_METHOD') == 'OPTIONS':
        print(json.dumps({"success": True}))
        return
    
    # Only allow DELETE requests
    if os.environ.get('REQUEST_METHOD') != 'DELETE':
        print(json.dumps({"success": False, "error": "Method not allowed"}))
        return
    
    try:
        # Check authorization header
        auth_header = os.environ.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            print(json.dumps({"success": False, "error": "Missing or invalid authorization"}))
            return
            
        auth_token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        if not validate_auth_token(auth_token):
            print(json.dumps({"success": False, "error": "Invalid auth token"}))
            return
        
        # Read DELETE data
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        if content_length == 0:
            print(json.dumps({"success": False, "error": "No data received"}))
            return
            
        post_data = sys.stdin.read(content_length)
        data = json.loads(post_data)
        
        if 'user_id' not in data:
            print(json.dumps({"success": False, "error": "Missing user_id"}))
            return

        user_id = data['user_id']
        
        if delete_profile_from_db(user_id):
            print(json.dumps({"success": True, "message": "Profile deleted successfully"}))
        else:
            print(json.dumps({"success": False, "error": "Profile not found or deletion failed"}))
            
    except json.JSONDecodeError:
        print(json.dumps({"success": False, "error": "Invalid JSON data"}))
    except Exception as e:
        print(json.dumps({"success": False, "error": "Internal server error"}))

if __name__ == "__main__":
    main()