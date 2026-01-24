@echo off
title Install AI Agent Requirements
color 0e
echo ==========================================
echo      INSTALLING AI AGENT LIBRARIES
echo ==========================================
echo.
echo 1. Installing Python Libraries...
pip install -r requirements.txt
echo.
echo 2. Installing Browser (Playwright)...
playwright install
echo.
echo ==========================================
echo      INSTALLATION COMPLETE!
echo ==========================================
echo.
echo You can now run 'Click_To_Start.bat'
pause
