from app import app
from flask import Flask, render_template, request, redirect
import os
import psycopg2
# from google.cloud import storage
from psycopg2 import sql, OperationalError

# Database connection details (replace with your values)
DB_HOST = "34.122.217.200"
DB_NAME = "myappdb"
DB_USER = "myuser"
DB_PASSWORD = 'mypassword'

# Route to insert data into the database
@app.route("/insert", methods=['POST'])
def insert_data():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        gender = request.form['gender']

        # Insert form data into the database
        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = conn.cursor()

            # Insert the data into your table (replace 'users' with your table name)
            cursor.execute("INSERT INTO users (name, gender) VALUES (%s, %s)", (name, gender))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            return redirect('/fetch')  # Redirect to the fetch route to see the updated data

        except Exception as e:
            return f"An error occurred: {e}"

# Route to fetch data from the database
@app.route("/fetch", methods=['GET'])
def fetch_data():
    # Fetch users from the database
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Select all users from the 'users' table
        cursor.execute("SELECT name, gender FROM users")
        users = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

    except Exception as e:
        users = []
        print(f"Error fetching users: {e}")

    return render_template("index.html", users=users)

def check_db_connection():
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Execute a simple query to test the connection
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        
        # Check if the result is as expected
        if result == (1,):
            print("Connection to the database is successful!")
        else:
            print("Connection test failed.")
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
    except OperationalError as e:
        print(f"Failed to connect to the database: {e}")

check_db_connection()