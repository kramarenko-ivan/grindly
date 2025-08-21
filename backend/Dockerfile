# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container first
# This leverages Docker's layer caching, speeding up future builds
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code from the 'app' directory into the container
COPY ./app ./app

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the Uvicorn server
# This tells Uvicorn to run the 'app' object from the 'main.py' file within the 'app' directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
