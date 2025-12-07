@echo off

REM Create a virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file
if exist .env goto EnvExists
set /p api_key="Please enter your Google Gemini API Key: "
echo GEMINI_API_KEY=%api_key% > .env
echo .env file created.
goto EndEnv

:EnvExists
echo .env file already exists. Skipping generation.

:EndEnv
echo Setup complete. You can now run the game using run.bat
