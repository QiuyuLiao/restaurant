import sqlite3
import os

# Define the path to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'restaurant.db')

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# User-related functions
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
    finally:
        conn.close()

def get_all_users():
    conn = get_db_connection()
    try:
        users = conn.execute("SELECT * FROM userdata").fetchall()
        return [dict(user) for user in users]
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT * FROM userdata WHERE email = ?", (email,)).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM userdata WHERE email = ? AND password = ?", (email, password)
        ).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

def update_user(userid, username, phone_number, is_admin):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            UPDATE userdata
            SET username = ?, phone_number = ?, isAdmin = ?
            WHERE userid = ?
            """,
            (username, phone_number, is_admin, userid),
        )
        conn.commit()
    finally:
        conn.close()

def delete_user(userid):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM userdata WHERE userid = ?", (userid,))
        conn.commit()
    finally:
        conn.close()

# Table-related functions
def add_table(isAvailable, capacity):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            INSERT INTO tables (isAvailable, capacity)
            VALUES (?, ?)
            """,
            (isAvailable, capacity),
        )
        conn.commit()
    finally:
        conn.close()

def get_all_tables():
    conn = get_db_connection()
    try:
        tables = conn.execute("""
            SELECT 
                t.table_id, 
                t.isAvailable, 
                t.capacity, 
                t.reserved_by,
                u.username AS reserved_by_username
            FROM tables t
            LEFT JOIN userdata u ON t.reserved_by = u.userid
        """).fetchall()
        return [dict(table) for table in tables]
    finally:
        conn.close()

def update_table(table_id, isAvailable, capacity):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            UPDATE tables
            SET isAvailable = ?, capacity = ?
            WHERE table_id = ?
            """,
            (isAvailable, capacity, table_id),
        )
        conn.commit()
    finally:
        conn.close()

def delete_table(table_id):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM tables WHERE table_id = ?", (table_id,))
        conn.commit()
    finally:
        conn.close()

# Reservation-related functions
def reserve_table(user_id, table_id):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            UPDATE tables
            SET isAvailable = 0, reserved_by = ?
            WHERE table_id = ? AND isAvailable = 1
            """,
            (user_id, table_id),
        )
        conn.commit()

        # Log the reservation in order_history
        conn.execute(
            """
            INSERT INTO order_history (user_id, table_id)
            VALUES (?, ?)
            """,
            (user_id, table_id),
        )
        conn.commit()
    finally:
        conn.close()

def cancel_reservation(user_id, table_id):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            UPDATE tables
            SET isAvailable = 1, reserved_by = NULL
            WHERE table_id = ? AND reserved_by = ?
            """,
            (table_id, user_id),
        )
        conn.commit()
    finally:
        conn.close()

# Order History functions
def get_user_order_history(user_id):
    conn = get_db_connection()
    try:
        history = conn.execute(
            """
            SELECT oh.order_id, oh.reserved_at, t.table_id, t.capacity
            FROM order_history oh
            JOIN tables t ON oh.table_id = t.table_id
            WHERE oh.user_id = ?
            ORDER BY oh.reserved_at DESC
            """,
            (user_id,),
        ).fetchall()
        return [dict(record) for record in history]
    finally:
        conn.close()

# Review-related functions
def add_review(user_id, table_id, review_text):
    conn = get_db_connection()
    try:
        conn.execute(
            """
            INSERT INTO reviews (user_id, table_id, review_text)
            VALUES (?, ?, ?)
            """,
            (user_id, table_id, review_text),
        )
        conn.commit()
    finally:
        conn.close()

def get_reviews_by_table(table_id):
    conn = get_db_connection()
    try:
        reviews = conn.execute(
            """
            SELECT r.review_text, u.username, r.created_at
            FROM reviews r
            JOIN userdata u ON r.user_id = u.userid
            WHERE r.table_id = ?
            ORDER BY r.created_at DESC
            """,
            (table_id,),
        ).fetchall()
        return [dict(review) for review in reviews]
    finally:
        conn.close()
