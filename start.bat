@echo off
setlocal
cd /d "C:\Users\stige\Desktop\yidaotech-new"

echo ==========================================
echo   yidaotech.cn - Astro Setup & Dev Server
echo ==========================================

:: Check Node.js
echo.
echo [1/3] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found in PATH.
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo        Node.js OK

:: Install dependencies (only if node_modules missing)
echo.
echo [2/3] Installing dependencies...
if not exist "node_modules" (
    npm install
    if errorlevel 1 (
        echo [ERROR] npm install failed.
        pause
        exit /b 1
    )
) else (
    echo        node_modules exists, skipping install.
)

:: Start dev server
echo.
echo [3/3] Starting dev server...
echo.
echo   Open http://localhost:4321 in your browser
echo   Press Ctrl+C to stop
echo ==========================================
echo.
npm run dev

pause
