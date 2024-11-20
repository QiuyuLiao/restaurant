import sqlite3
import os

# Define the path to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'restaurant.db')

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# Function to add a new user
def add_user(email, username, password, phone_number, is_admin=False):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            INSERT INTO userdata (email, username, password, phone_number, isAdmin)
            VALUES (?, ?, ?, ?, ?)
            """,
            (email, username, password, phone_number, is_admin),
        )
        conn.commit()
        print(f"User {username} added successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error adding user: {e}")
    finally:
        conn.close()

# Function to fetch all users
def get_all_users():
    conn = get_db_connection()
    try:
        users = conn.execute("SELECT * FROM userdata").fetchall()
        return [dict(user) for user in users]
    finally:
        conn.close()

# Function to fetch a user by email
def get_user_by_email(email):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT * FROM userdata WHERE email = ?", (email,)).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()
