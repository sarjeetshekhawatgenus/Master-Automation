@echo off
setlocal enabledelayedexpansion

echo ================================================================
echo   Building MasterAutomation Windows Application (.exe)
echo ================================================================

cd /d "%~dp0"

echo [1/3] Checking environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [2/3] Checking dependencies...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo [3/3] Compiling with PyInstaller...
python -m PyInstaller --noconfirm --clean MasterAutomation.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed. Please check the logs above.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo   Build Successful!
echo   Executable location: dist\MasterAutomation\MasterAutomation.exe
echo ================================================================
echo.
pause
