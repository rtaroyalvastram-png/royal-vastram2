@echo off
setlocal EnableDelayedExpansion
TITLE Royal Vastram Launcher
color 0A

:: Force script to run from its own directory
cd /d "%~dp0"

echo ==================================================
echo      ROYAL VASTRAM - BILLING SYSTEM
echo ==================================================
echo.

:: 0. Check Prerequisites
echo [0/5] Checking System...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ and check "Add to PATH".
    pause
    exit /b
)

:: 1. Update
echo [1/5] Updating...
ping -n 1 8.8.8.8 >nul 2>&1
if !errorlevel! neq 0 (
    echo    ! Offline mode: No internet connection. Skipping update.
) else (
    echo    > Checking for updates...
    git pull origin main
    if !errorlevel! neq 0 (
        echo.
        echo    ! UPDATE FAILED: You have local changes that prevent automatic update.
        echo    ! Using your current local version.
    ) else (
        echo    > Updated successfully.
    )
)
echo.

:: 2. Backend Setup
echo [2/5] Setting up Backend...
if not exist "backend" (
    echo [ERROR] 'backend' folder missing in %cd%
    pause
    exit /b
)

cd backend
if not exist "venv" (
    echo    > Creating venv...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [ERROR] Could not create venv.
        pause
        exit /b
    )
)

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] venv corrupt. Deleting...
    rmdir /s /q venv
    echo Please run again.
    pause
    exit /b
)

call venv\Scripts\activate
if !errorlevel! neq 0 (
    echo [ERROR] Failed to activate venv.
    pause
    exit /b
)

echo    > Installing dependencies...
pip install -q -r requirements.txt
cd ..
echo.

:: 3. Frontend Setup
echo [3/5] Setting up Frontend...
cd frontend
if not exist "node_modules" (
    echo    > Installing Node Modules...
    call npm ci
)
cd ..
echo.

:: 4. Launch
echo [4/5] Launching...
start "Backend" cmd /k "cd backend && call venv\Scripts\activate && uvicorn main:app --reload"
timeout /t 2 >nul
start "Frontend" cmd /k "cd frontend && npm run dev"

:: 5. Browser
echo [5/5] Done!
timeout /t 4 >nul
start http://localhost:5173

echo.
echo ====================================
echo    APP IS RUNNING!
echo    Keep this window open.
echo ====================================
pause
