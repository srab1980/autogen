# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy frontend source
COPY autogen/python/packages/autogen-studio/frontend/package*.json ./
RUN npm install

COPY autogen/python/packages/autogen-studio/frontend ./
RUN npm run build

# Stage 2: Final Image
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY autogen/python/packages/autogen-studio /app/autogen-studio

# Copy built frontend assets to the python package UI directory
# Ensure the target directory exists
RUN mkdir -p /app/autogen-studio/autogenstudio/web/ui
# Overlay built assets
COPY --from=frontend-builder /app/frontend/public /app/autogen-studio/autogenstudio/web/ui

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
