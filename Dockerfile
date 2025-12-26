FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy local source code
# We copy the 'autogen' directory which contains all packages
COPY autogen /app/autogen

# Install packages from local source in dependency order
# 1. Autogen Core
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e /app/autogen/python/packages/autogen-core

# 2. Autogen AgentChat (depends on core)
RUN pip install --no-cache-dir -e /app/autogen/python/packages/autogen-agentchat

# 3. Autogen Ext (depends on core, agentchat)
RUN pip install --no-cache-dir -e /app/autogen/python/packages/autogen-ext

# 4. Autogen Studio (depends on all above)
RUN pip install --no-cache-dir -e /app/autogen/python/packages/autogen-studio

# Expose the port
EXPOSE 8081

# Set the entrypoint
# We look for the main database in the mounted volume
ENV AUTOGENSTUDIO_DATABASE_URI="sqlite:////app/data/autogen04202.db"
ENV AUTOGENSTUDIO_APPDIR="/app/data"

# Create a directory for data
RUN mkdir -p /app/data

# Copy the database from the root to the data directory
COPY autogen04202.db /app/data/autogen04202.db


# Command to run the application
# Command to run the application
# We use shell form to allow variable expansion for PORT (default 8081)
CMD autogenstudio ui --host 0.0.0.0 --port ${PORT:-8081}
