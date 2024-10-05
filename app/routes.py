from app import app
from flask import Flask, render_template, request, redirect, jsonify
import os
import psycopg2
from google.cloud import storage
from psycopg2 import sql, OperationalError


# Google Cloud Storage bucket name
GCP_BUCKET_NAME = "my-bucket-0511"

# Database connection details (replace with your values)
DB_HOST = "34.72.76.71"
DB_NAME = "myappdb"
DB_USER = "myuser"
DB_PASSWORD = 'mypassword'


# Initialize the Google Cloud Storage client
def upload_to_gcp_bucket(file, bucket_name):
    """Uploads a file to the given GCP bucket."""
    try:
        # Create a storage client
        storage_client = storage.Client()

        # Get the bucket
        bucket = storage_client.bucket(bucket_name)

        # Create a new blob and upload the file's content
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)

        # Return the blob's public URL based on the bucket's permissions
        return f"https://storage.googleapis.com/{bucket_name}/{file.filename}"

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Route to insert data into the database
@app.route("/insert", methods=['POST'])
def insert_data():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        gender = request.form.get('gender')

        # Check if form data is complete
        if not name or not gender:
            return jsonify({"error": "Missing name or gender"}), 400  # 400 Bad Request

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
            cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        gender VARCHAR(10)
    );
""")

            cursor.execute("INSERT INTO users (name, gender) VALUES (%s, %s)", (name, gender))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            return jsonify({"message": "Data inserted successfully!"}), 201  # 201 Created

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # 500 Internal Server Error

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
        print(jsonify({"error": e}), 500 )
        
    
    if not users:  # Check if the users list is empty
        message = "No users found."
    else:
        message = ""  # Return an empty string if users are found

    return jsonify({"Users": users, "message": message}), 200 



@app.route("/upload-to-bucket", methods=['GET', 'POST'])
def upload_to_bucket():
    if request.method == 'POST':
        # Check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']

        # If no file is selected
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400 

        if file:
            # Upload file to GCP bucket
            public_url = upload_to_gcp_bucket(file, GCP_BUCKET_NAME)

            if public_url:
                return jsonify({"message": "File uploaded successfully!", "url": public_url}), 200 
            else:
                return jsonify({"error": "Failed to upload file"}), 500 








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