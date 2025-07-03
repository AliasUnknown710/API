import sys
import requests
import mysql.connector

API_BASE_URL = "https://your-api-domain.com/api"
DELETE_PROFILE_ENDPOINT = "/users/delete_profile"
DB_CONFIG = {
    "host": "localhost",
    "user": "your_db_user",
    "password": "your_db_password",
    "database": "your_db_name"
}  # Update these values

def delete_profile_from_db(user_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Profile deleted from database.")
        else:
            print("No profile found in database.")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def delete_profile(user_id, auth_token):
    url = f"{API_BASE_URL}{DELETE_PROFILE_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    data = {"user_id": user_id}
    response = requests.delete(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Profile deleted via API.")
        delete_profile_from_db(user_id)
    else:
        print(f"Failed to delete profile via API: {response.status_code} {response.text}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python delete_profile.py <user_id> <auth_token>")
        sys.exit(1)
    user_id = sys.argv[1]
    auth_token = sys.argv[2]
    delete_profile(user_id, auth_token)