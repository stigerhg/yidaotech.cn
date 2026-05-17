@echo off
setlocal
cd /d "C:\Users\stige\Desktop\yidaotech-new"

echo ==========================================
echo   yidaotech.cn - First Time Setup
echo ==========================================
echo.
echo This will install all dependencies.
echo This only needs to run once.
echo.

node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Install from https://nodejs.org
    pause
    exit /b 1
)

echo Installing npm packages...
call npm install

if errorlevel 1 (
    echo.
    echo [ERROR] npm install failed.
    echo Try running: npm install --legacy-peer-deps
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Setup complete!
echo.
echo   Run start.bat to launch the dev server
echo   or run: npm run dev
echo ==========================================
echo.
pause
