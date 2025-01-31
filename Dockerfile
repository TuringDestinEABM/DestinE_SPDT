# Base image
FROM python:3.9.0-slim

# Set working directory
WORKDIR /digitalTwin

# Copy the Flask app to the container
COPY . .

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port on which the app will run
EXPOSE 5000