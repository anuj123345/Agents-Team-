@echo off
title Agent Teams UI — Local Server
color 0B
echo.
echo  ============================================
echo   Agent Teams UI — Starting local server...
echo  ============================================
echo.

set PORT=8080
set DIR=%~dp0

:: Try Python 3 first (uses proxy_server.py for NVIDIA API proxying)
python --version >nul 2>&1
if %errorlevel%==0 (
    echo  [OK] Found Python. Starting proxy server on http://localhost:%PORT%
    echo  [OK] Opening browser...
    cd /d "%DIR%"
    timeout /t 1 /nobreak >nul
    start "" "http://localhost:%PORT%/agent-teams-ui.html"
    echo.
    python proxy_server.py
    goto :done
)

:: Try Python 3 via py launcher
py --version >nul 2>&1
if %errorlevel%==0 (
    echo  [OK] Found Python (py launcher). Starting proxy server on http://localhost:%PORT%
    cd /d "%DIR%"
    timeout /t 1 /nobreak >nul
    start "" "http://localhost:%PORT%/agent-teams-ui.html"
    echo.
    py proxy_server.py
    goto :done
)

:: Try Node.js / npx
node --version >nul 2>&1
if %errorlevel%==0 (
    echo  [OK] Found Node.js. Starting server on http://localhost:%PORT%
    timeout /t 1 /nobreak >nul
    start "" "http://localhost:%PORT%/agent-teams-ui.html"
    echo.
    npx --yes serve "%DIR%" -p %PORT% -s
    goto :done
)

:: Nothing found
echo  [ERROR] Could not find Python or Node.js on this machine.
echo.
echo  Please install one of the following:
echo    - Python  : https://www.python.org/downloads/
echo    - Node.js : https://nodejs.org/
echo.
echo  Then double-click start.bat again.
echo.
pause
goto :done

:done
