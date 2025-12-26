# Deploying AutoGen Studio

This guide explains how to deploy AutoGen Studio to various platforms including Coolify, Fly.io, and other deployment platforms that support Nixpacks or Docker.

## Overview

This repository is now configured to work with:
- **Coolify** (using Nixpacks or Docker)
- **Fly.io** (using Dockerfile)
- **Heroku** (using Procfile)
- **Railway** (auto-detection)
- Any platform supporting Python Buildpacks or Docker

## Required Files

The repository includes these deployment configuration files:

- `requirements.txt` - Python dependencies (autogenstudio)
- `Procfile` - Process definition for platforms like Heroku
- `runtime.txt` - Python version specification (3.11)
- `main.py` - Application entry point with environment variable support
- `Dockerfile` - Docker container definition

## Deploying to Coolify

Coolify will automatically detect this as a Python application using Nixpacks.

1. **Connect Repository** in Coolify dashboard
2. **Configure Environment Variables** (optional):
   - `PORT` - The port to run on (auto-configured by Coolify)
   - `HOST` - The host to bind to (defaults to 0.0.0.0)
   - `OPENAI_API_KEY` - Your OpenAI API key (if needed)
   - `AUTOGENSTUDIO_DATABASE_URI` - Database location (defaults to /app/data/autogen04202.db)
   
3. **Deploy** - Coolify will use Nixpacks to:
   - Detect Python 3.11 from runtime.txt
   - Install dependencies from requirements.txt
   - Start the app using the Procfile command

## Deploying to Fly.io

This guide explains how to deploy your modified AutoGen Studio application to Fly.io using the Dockerfile we prepared.

### Prerequisites
1.  **Fly.io Account**: Sign up at [fly.io](https://fly.io/).
2.  **flyctl installed**: [Install flyctl](https://fly.io/docs/hands-on/install-flyctl/).
    *   Windows (PowerShell): `pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"`

### Steps using `fly launch` (Recommended)

1.  **Login to Fly.io**:
    ```powershell
    fly auth login
    ```

2.  **Initialize the App**:
    Run this command in the root folder:
    ```powershell
    fly launch
    ```
    *   It will detect the `Dockerfile`.
    *   It will ask you to copy the configuration (say **Yes**).
    *   It will ask for an **App Name** (e.g., `my-autogen-studio`).
    *   It will ask for a **Region** (choose one close to you).
    *   It might ask to set up a Database (say **No**, unless you want Postgres).

3.  **Set Secrets (API Keys)**:
    Before deploying, you MUST set your OpenAI API Key on the server:
    ```powershell
    fly secrets set OPENAI_API_KEY=sk-your-key-here
    ```
    Environment variable override:
    ```powershell
    fly secrets set OPENAI_BASE_URL=https://api.openai.com/v1
    ```

4.  **Deploy**:
    ```powershell
    fly deploy
    ```

5.  **Visit your App**:
    ```powershell
    fly open
    ```

### Alternative: Deploy directly from GitHub
Since we have pushed the `Dockerfile` to your repository, you can deploy directly from there.

1.  **Create App** (if not done):
    ```powershell
    fly apps create my-autogen-studio
    ```

2.  **Deploy Command**:
    ```powershell
    fly deploy https://github.com/srab1980/autogen.git
    ```
    *Or configure "Continuous Deployment" in the Fly.io Dashboard to auto-deploy when you push changes to main.*

3.  **Important**: You must still set the secrets!
    ```powershell
    fly secrets set OPENAI_API_KEY=sk-... OPENAI_BASE_URL=https://api.openai.com/v1 -a my-autogen-studio
    ```

## Deploying with Docker Locally

You can also run this using Docker on your local machine or any Docker-compatible environment:

```bash
# Build the image
docker build -t autogen-studio .

# Run the container
docker run -p 8081:8081 \
  -v $(pwd)/data:/app/data \
  -e OPENAI_API_KEY=your-key-here \
  autogen-studio
```

Or using docker-compose:

```bash
docker-compose up -d
```

## Troubleshooting

### Nixpacks Detection Issues
If Nixpacks fails to detect the application type:
- Ensure `requirements.txt` exists at the repository root
- Check that `runtime.txt` specifies a valid Python version
- Verify the `Procfile` has the correct web process definition

### Port Configuration
- Coolify/Nixpacks: Uses the `PORT` environment variable automatically
- Fly.io: Configure port in fly.toml or use environment variables
- Docker: Port 8081 is exposed by default, map it with `-p` flag

### Database Persistence
The application uses SQLite by default. To persist data:
- Mount a volume at `/app/data` (Docker)
- Configure volume persistence in your deployment platform
- Set `AUTOGENSTUDIO_DATABASE_URI` environment variable for custom database location
