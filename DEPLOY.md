# Deploying AutoGen Studio to Fly.io

This guide explains how to deploy your modified AutoGen Studio application to Fly.io using the Dockerfile we prepared.

## Prerequisites
1.  **Fly.io Account**: Sign up at [fly.io](https://fly.io/).
2.  **flyctl installed**: [Install flyctl](https://fly.io/docs/hands-on/install-flyctl/).
    *   Windows (PowerShell): `pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"`

## Steps using `fly launch` (Recommended)

1.  **Login to Fly.io**:
    ```powershell
    fly auth login
    ```

2.  **Initialize the App**:
    Run this command in the root folder (`Downloads\AutoGen Studio`):
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

## Alternative: Deploy directly from GitHub
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
