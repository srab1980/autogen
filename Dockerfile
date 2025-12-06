# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
# Copy entire context to debug/ensure availability
# Copy entire context to debug/ensure availability
COPY . /app/source/
# DEBUG: List all files to see what was copied
RUN find /app/source -maxdepth 2 -not -path '*/.*'
WORKDIR /app/source/autogen/python/packages/autogen-studio/frontend
RUN npm install
RUN npm run build

# Stage 2: Final Image
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code FROM THE SOURCE STAGE (ensuring we have it)
COPY --from=frontend-builder /app/source/autogen/python/packages/autogen-studio /app/autogen-studio

# Copy built frontend assets to the python package UI directory
# Ensure the target directory exists
RUN mkdir -p /app/autogen-studio/autogenstudio/web/ui
# Overlay built assets
COPY --from=frontend-builder /app/source/autogen/python/packages/autogen-studio/frontend/public /app/autogen-studio/autogenstudio/web/ui

# Install the package
WORKDIR /app/autogen-studio
RUN pip install --no-cache-dir .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Run the application
CMD ["autogenstudio", "ui", "--host", "0.0.0.0", "--port", "8080"]
