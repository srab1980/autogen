FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python packages from PyPI
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py /app/

# Expose the port
EXPOSE 8081

# Set the entrypoint
# We look for the main database in the mounted volume
ENV AUTOGENSTUDIO_DATABASE_URI="sqlite:////app/data/autogen04202.db"
ENV AUTOGENSTUDIO_APPDIR="/app/data"

# Create a directory for data
RUN mkdir -p /app/data

# Command to run the application using the configurable entry point
CMD ["python", "main.py"]
