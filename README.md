# Custom AutoGen Studio Environment

This repository contains a customized environment for running **AutoGen Studio**, including a specific database configuration (`autogen04202.db`) and a suite of maintenance scripts.

## Overview

This application serves as a workspace for developing and deploying multi-agent AI workflows using the Microsoft AutoGen framework. It wraps the core AutoGen libraries (located in `autogen/`) with custom data and tooling.

Key components:
- **`autogen04202.db`**: The SQLite database acting as the source of truth for agents, workflows, and sessions.
- **`launch_autogen_studio.ps1`**: A PowerShell script to launch the studio locally.
- **Maintenance Scripts**: Various Python scripts (`check_*.py`, `fix_*.py`, `dump_*.py`) for database inspection and data migration.
- **Deployment Config**: `Dockerfile` and `DEPLOY.md` for deploying to Fly.io.

## Prerequisites

- **Python 3.11+**
- **PowerShell** (for Windows scripts)
- **Git**

## Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment:**
    The launch script expects a virtual environment named `.venv_new`.
    ```bash
    python -m venv .venv_new
    ```

3.  **Activate the Virtual Environment:**
    - Windows (PowerShell):
      ```powershell
      .\.venv_new\Scripts\Activate.ps1
      ```
    - Linux/macOS:
      ```bash
      source .venv_new/bin/activate
      ```

4.  **Install Dependencies:**
    Install the AutoGen packages from the local `autogen` submodule in editable mode.
    ```bash
    pip install --upgrade pip
    pip install -e autogen/python/packages/autogen-core
    pip install -e autogen/python/packages/autogen-agentchat
    pip install -e autogen/python/packages/autogen-ext
    pip install -e autogen/python/packages/autogen-studio
    ```

## Running the Application

To start the AutoGen Studio UI locally:

1.  Ensure you have your OpenAI API key ready.
2.  Run the launch script (Windows):
    ```powershell
    .\launch_autogen_studio.ps1
    ```
    *Note: You may need to set your `OPENAI_API_KEY` environment variable or modify the script to include it if not already set globally.*

    The script sets the database URI to the local `autogen04202.db` file and starts the server on port `8081`.

3.  Access the UI at `http://localhost:8081`.

## Deployment

For instructions on deploying this application to **Fly.io**, please refer to [DEPLOY.md](DEPLOY.md).

## Maintenance Scripts

The root directory contains several utility scripts for managing the AutoGen database and configurations.

-   **`check_*.py`**: Diagnostic scripts.
    -   `check_db.py`: Inspects the `team` table and prints agent/model configurations.
    -   `check_component_versions.py`: Verifies the versions of installed AutoGen components.
    -   `check_all_tables.py`: Lists all tables in the database.
-   **`fix_*.py`**: Repair scripts.
    -   Used to patch or migrate data within the database (e.g., `fix_model_info.py`).
-   **`dump_*.py`**: Export scripts.
    -   Dumps specific data from the database to JSON files (e.g., `dump_teams.py`).
-   **`inspect_*.py`**: Inspection scripts.
    -   Deep dive into specific database entries (e.g., `inspect_db_deep.py`).

## Database

The primary database file is **`autogen04202.db`**.
-   **Backup**: `autogen04202.db.bak`
-   **Connection String**: `sqlite:///autogen04202.db`

When running locally, the application directly reads/writes to this file. In the Docker container, this file is copied to `/app/data/`.
