@echo off
title AI Browser Agent
color 0A

echo ==================================================
echo          STARTING AI BROWSER AGENT
echo ==================================================
echo.

:: 1. Check/Ask for API Key
if "%GOOGLE_API_KEY%"=="" (
    if "%OPENAI_API_KEY%"=="" (
        echo [SETUP] We need your API Key to see the browser.
        echo.
        set /p GKEY="Please Paste your Google Gemini API Key: "
        set GOOGLE_API_KEY=%GKEY%
        echo.
        echo Great! Key saved for this session.
        echo.
    )
)

:: 2. Run the App
python AgentApp.py

:: 3. Error Handling
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The App closed unexpectedly.
    echo If this is the first time, make sure you ran 'Install_Dependencies.bat' first.
    pause
)
