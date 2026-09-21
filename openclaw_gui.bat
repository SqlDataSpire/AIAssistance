@echo off
title OpenClaw Web UI Launcher
setlocal enabledelayedexpansion

:: ============================================================================
:: CONFIGURATION
:: ============================================================================
set "REMOTE_USER=root"
set "REMOTE_HOST=192.168.1.199"
set "REMOTE_PORT=18789"
set "LOCAL_PORT=18789"
set "CHROME_PROFILE=%TEMP%\openclaw_chrome_session"
set "WINDOW_TITLE=OpenClaw SSH Tunnel (Do Not Close)"

:: ============================================================================
:: 1. LOCATE GOOGLE CHROME
:: ============================================================================
set "CHROME_EXE="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set "CHROME_EXE=C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set "CHROME_EXE=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set "CHROME_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

if "%CHROME_EXE%"=="" (
    echo [ERROR] Google Chrome was not found in standard installation paths.
    echo Please install Chrome or update the CHROME_EXE path in this script.
    pause
    exit /b 1
)

:: ============================================================================
:: 2. OPEN SSH TUNNEL
:: ============================================================================
echo ============================================================================
echo  Starting SSH Tunnel to %REMOTE_USER%@%REMOTE_HOST%...
echo ============================================================================
echo.
echo  Please enter your password in the pop-up SSH window...
echo.

start "%WINDOW_TITLE%" ssh -L %LOCAL_PORT%:127.0.0.1:%REMOTE_PORT% -N %REMOTE_USER%@%REMOTE_HOST%

:: ============================================================================
:: 3. WAIT UNTIL PASSWORD IS ENTERED & TUNNEL IS LISTENING
:: ============================================================================
echo Waiting for password authentication and port %LOCAL_PORT% to open...

:WAIT_TUNNEL
:: Check if port 18789 is active and listening
netstat -aon | findstr /r /c:":%LOCAL_PORT% .*LISTENING" >nul 2>&1
if not errorlevel 1 goto TUNNEL_READY

:: Check if the SSH process died (e.g. wrong password or window closed)
tasklist /FI "IMAGENAME eq ssh.exe" 2>nul | findstr /I "ssh.exe" >nul
if errorlevel 1 (
    echo.
    echo [ERROR] SSH window was closed or connection failed before tunnel opened.
    pause
    exit /b 1
)

timeout /t 1 /nobreak >nul
goto WAIT_TUNNEL

:TUNNEL_READY
echo.
echo [SUCCESS] Password authenticated! SSH Tunnel is active on port %LOCAL_PORT%.

:: ============================================================================
:: 4. LAUNCH CHROME & WAIT FOR BROWSER TO CLOSE
:: ============================================================================
echo.
echo Opening OpenClaw Web UI at http://localhost:%LOCAL_PORT%...
echo The script is now waiting for you to close the OpenClaw browser window...
echo.

start /wait "" "%CHROME_EXE%" --app=http://localhost:%LOCAL_PORT% --user-data-dir="%CHROME_PROFILE%"

:: ============================================================================
:: 5. CLEANUP SSH TUNNEL & TEMP FILES ON EXIT
:: ============================================================================
echo.
echo Browser window closed. Terminating SSH Tunnel...

for /f "tokens=5" %%a in ('netstat -aon ^| findstr /r /c:":%LOCAL_PORT% .*LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

if exist "%CHROME_PROFILE%" (
    rmdir /s /q "%CHROME_PROFILE%" >nul 2>&1
)

echo.
echo ============================================================================
echo  OpenClaw session closed cleanly.
echo ============================================================================
timeout /t 2 >nul
exit /b 0
