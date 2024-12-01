# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install system dependencies (e.g., for MySQL client libraries)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies via setup.py
RUN pip install --no-cache-dir .

# Expose the Flask port
EXPOSE 5001:5001

# Command to run the application
CMD ["python", "run.py"]