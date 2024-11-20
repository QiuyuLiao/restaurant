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

# Create User table with a phone_number attribute
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

print("User table with phone_number created successfully.")

# Commit and close the connection
conn.commit()
conn.close()
