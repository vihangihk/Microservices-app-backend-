# Use the official Python image from Docker Hub as the base image
FROM python:3.10-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code to the working directory
COPY . .

# Expose port 5000 (Flask's default port)
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]
