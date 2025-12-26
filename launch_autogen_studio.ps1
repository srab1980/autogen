$env:AUTOGENSTUDIO_DATABASE_URI="sqlite:///autogen04202.db"
$env:OPENAI_BASE_URL="https://api.openai.com/v1"
Write-Host "Starting AutoGen Studio with database: $env:AUTOGENSTUDIO_DATABASE_URI"
Write-Host "Using OpenAI Base URL: $env:OPENAI_BASE_URL"
.\.venv_new\Scripts\autogenstudio ui --port 8081
