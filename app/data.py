#!/usr/bin/env python3
import sqlite3
import os

# Define the directory path where you want to create the database
database_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
os.makedirs(database_dir, exist_ok=True)

# Path to the database file
db_path = os.path.join(database_dir, 'restaurant.db')

# Connect to the database
conn = sqlite3.connect(db_path)
curr = conn.cursor()

# Create User table
curr.execute("""
CREATE TABLE IF NOT EXISTS userdata(
    userid INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    isAdmin BOOLEAN NOT NULL DEFAULT 0
)
""")

# Create Tables table
curr.execute("""
CREATE TABLE IF NOT EXISTS tables(
    table_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isAvailable BOOLEAN NOT NULL DEFAULT 1,
    capacity INTEGER NOT NULL,
    reserved_by INTEGER DEFAULT NULL,
    FOREIGN KEY (reserved_by) REFERENCES userdata(userid) ON DELETE SET NULL
)
""")

# Create Order History table
curr.execute("""
CREATE TABLE IF NOT EXISTS order_history(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    table_id INTEGER NOT NULL,
    reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES userdata(userid) ON DELETE CASCADE,
    FOREIGN KEY (table_id) REFERENCES tables(table_id) ON DELETE CASCADE
)
""")

# Create Reviews table
curr.execute("""
CREATE TABLE IF NOT EXISTS reviews(
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    table_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES userdata(userid) ON DELETE CASCADE,
    FOREIGN KEY (table_id) REFERENCES tables(table_id) ON DELETE CASCADE
)
""")

print("Database setup completed successfully.")

# Commit and close the connection
conn.commit()
conn.close()
