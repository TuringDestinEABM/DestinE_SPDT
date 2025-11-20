# Base image
FROM python:3.13.5

# Set working directory
WORKDIR /digitalTwin

# Copy requirements.txt separately to avoid invalidating cache
COPY requirements.txt /tmp/

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

# Copy the Flask app to the container
COPY . .


# Expose the port on which the app will run
EXPOSE 5000