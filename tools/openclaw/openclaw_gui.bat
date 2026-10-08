@echo off
setlocal EnableExtensions EnableDelayedExpansion
title OpenClaw Web UI Launcher

rem ===========================================================================
rem  OpenClaw Web UI launcher for Windows
rem
rem  For an OpenClaw gateway on a remote machine whose bind is set to loopback
rem  (local only). Opens an SSH tunnel, launches the Control UI in its own app
rem  window, and closes the tunnel when you close that window.
rem
rem  Usage:
rem    openclaw_gui.bat [user@]host [remote_port] [local_port]
rem    openclaw_gui.bat --help
rem
rem  Settings, highest priority first:
rem    1. Command-line arguments
rem    2. Environment variables (OPENCLAW_HOST, OPENCLAW_USER, ...)
rem    3. openclaw_gui.config.cmd in the same folder as this script
rem    4. Interactive prompts, with an offer to save a config file
rem ===========================================================================

set "SCRIPT_DIR=%~dp0"
set "CONFIG_FILE=%SCRIPT_DIR%openclaw_gui.config.cmd"
set "VARS=OPENCLAW_HOST OPENCLAW_USER OPENCLAW_SSH_PORT OPENCLAW_SSH_KEY OPENCLAW_REMOTE_PORT OPENCLAW_LOCAL_PORT OPENCLAW_BROWSER OPENCLAW_KEEP_PROFILE"
set "SSH_PID="
set "PROFILE_DIR="

if /i "%~1"=="--help" goto :usage
if /i "%~1"=="-h" goto :usage
if "%~1"=="/?" goto :usage

rem --- Config file first, then let environment variables override it --------
for %%V in (%VARS%) do if defined %%V set "_ENV_%%V=!%%V!"
if exist "%CONFIG_FILE%" call "%CONFIG_FILE%"
for %%V in (%VARS%) do if defined _ENV_%%V set "%%V=!_ENV_%%V!"

rem --- Command-line arguments override everything ----------------------------
if "%~1"=="" goto :args_done
set "_TARGET=%~1"
if "!_TARGET:@=!"=="!_TARGET!" goto :host_only
for /f "tokens=1,* delims=@" %%a in ("!_TARGET!") do (
    set "OPENCLAW_USER=%%a"
    set "OPENCLAW_HOST=%%b"
)
goto :args_ports
:host_only
set "OPENCLAW_HOST=!_TARGET!"
:args_ports
if not "%~2"=="" set "OPENCLAW_REMOTE_PORT=%~2"
if not "%~3"=="" set "OPENCLAW_LOCAL_PORT=%~3"
:args_done

rem --- Prompt for anything still missing -------------------------------------
set "_PROMPTED="
if defined OPENCLAW_HOST goto :have_host
echo No remote host configured.
set /p "OPENCLAW_HOST=Remote host running OpenClaw (IP or hostname): "
if not defined OPENCLAW_HOST goto :no_host
set /p "OPENCLAW_USER=SSH user (leave blank to use your SSH config or Windows user name): "
set "_PROMPTED=1"
:have_host

rem --- Defaults ---------------------------------------------------------------
if not defined OPENCLAW_SSH_PORT set "OPENCLAW_SSH_PORT=22"
if not defined OPENCLAW_REMOTE_PORT set "OPENCLAW_REMOTE_PORT=18789"
if not defined OPENCLAW_LOCAL_PORT set "OPENCLAW_LOCAL_PORT=!OPENCLAW_REMOTE_PORT!"

rem Ports must be digits only (no pipes here: !vars! don't expand inside a pipe).
for %%P in (OPENCLAW_SSH_PORT OPENCLAW_REMOTE_PORT OPENCLAW_LOCAL_PORT) do (
    set "_BAD="
    set "_VAL=!%%P!"
    if not defined _VAL set "_BAD=1"
    for /f "delims=0123456789" %%x in ("!_VAL!") do set "_BAD=1"
    if defined _BAD (
        echo [ERROR] %%P must be a number, got "!_VAL!".
        goto :fail
    )
)

rem --- Offer to save prompted settings ---------------------------------------
if not defined _PROMPTED goto :config_done
choice /c YN /n /m "Save these settings to openclaw_gui.config.cmd for next time? [Y/N] "
if errorlevel 2 goto :config_done
> "%CONFIG_FILE%" (
    echo @rem OpenClaw launcher settings. Created by openclaw_gui.bat - safe to edit.
    echo set "OPENCLAW_HOST=!OPENCLAW_HOST!"
    echo set "OPENCLAW_USER=!OPENCLAW_USER!"
    echo set "OPENCLAW_SSH_PORT=!OPENCLAW_SSH_PORT!"
    echo set "OPENCLAW_REMOTE_PORT=!OPENCLAW_REMOTE_PORT!"
    echo set "OPENCLAW_LOCAL_PORT=!OPENCLAW_LOCAL_PORT!"
)
echo Saved to "%CONFIG_FILE%".
:config_done

set "URL=http://localhost:!OPENCLAW_LOCAL_PORT!/"
if defined OPENCLAW_USER (set "SSH_TARGET=!OPENCLAW_USER!@!OPENCLAW_HOST!") else set "SSH_TARGET=!OPENCLAW_HOST!"

rem --- If something already listens on the local port, reuse or quit ---------
call :port_listening !OPENCLAW_LOCAL_PORT!
if errorlevel 1 goto :start_tunnel
echo.
echo [WARN] Local port !OPENCLAW_LOCAL_PORT! is already in use. A tunnel may already be open,
echo        or another program is using it. Pick another port with the third argument.
choice /c OQ /n /m "[O]pen the UI on the existing port, or [Q]uit? "
if errorlevel 2 goto :fail
goto :launch_ui

rem ===========================================================================
:start_tunnel
where ssh >nul 2>&1
if errorlevel 1 goto :no_ssh

set "SSH_ARGS=-N -L 127.0.0.1:!OPENCLAW_LOCAL_PORT!:127.0.0.1:!OPENCLAW_REMOTE_PORT! -p !OPENCLAW_SSH_PORT! -o ExitOnForwardFailure=yes -o ServerAliveInterval=30"
if defined OPENCLAW_SSH_KEY set "SSH_ARGS=!SSH_ARGS! -i "!OPENCLAW_SSH_KEY!""
set "SSH_ARGS=!SSH_ARGS! !SSH_TARGET!"

echo ============================================================================
echo  Starting SSH tunnel: localhost:!OPENCLAW_LOCAL_PORT! -^> !SSH_TARGET!:!OPENCLAW_REMOTE_PORT!
echo ============================================================================
echo  An SSH window will open. Enter your password or key passphrase there if asked.
echo  Leave that window open; it closes automatically when you're done.
echo.

rem Start ssh in its own window and capture its exact process ID.
for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "$p = Start-Process -FilePath ssh -ArgumentList $env:SSH_ARGS -PassThru; $p.Id"`) do set "SSH_PID=%%P"
if not defined SSH_PID goto :ssh_start_failed

echo Waiting for the tunnel on port !OPENCLAW_LOCAL_PORT! ...
set /a "_WAITED=0"
:wait_tunnel
call :port_listening !OPENCLAW_LOCAL_PORT!
if not errorlevel 1 goto :tunnel_ready
rem %SSH_PID% (not !SSH_PID!) because delayed expansion is off inside a pipe.
tasklist /FI "PID eq %SSH_PID%" 2>nul | findstr /I "ssh.exe" >nul
if errorlevel 1 goto :ssh_died
if !_WAITED! geq 300 goto :tunnel_timeout
timeout /t 1 /nobreak >nul
set /a "_WAITED+=1"
goto :wait_tunnel

:tunnel_ready
echo [OK] Tunnel is up.

rem ===========================================================================
:launch_ui
set "BROWSER_EXE="
if defined OPENCLAW_BROWSER if exist "!OPENCLAW_BROWSER!" set "BROWSER_EXE=!OPENCLAW_BROWSER!"
for %%B in (
    "%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
    "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
    "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
    "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
) do if not defined BROWSER_EXE if exist "%%~B" set "BROWSER_EXE=%%~B"
if not defined BROWSER_EXE goto :default_browser

rem A separate browser profile makes "start /wait" track this window only.
if defined OPENCLAW_KEEP_PROFILE (
    set "PROFILE_DIR=%LOCALAPPDATA%\openclaw_gui\profile"
    set "DELETE_PROFILE="
) else (
    set "PROFILE_DIR=%TEMP%\openclaw_gui_profile"
    set "DELETE_PROFILE=1"
)

echo.
echo Opening !URL!
echo Close the OpenClaw window to end the session and close the tunnel.
start "" /wait "!BROWSER_EXE!" --app=!URL! --user-data-dir="!PROFILE_DIR!" --no-first-run --no-default-browser-check
goto :cleanup

:default_browser
echo Chrome or Edge not found; opening your default browser.
start "" "!URL!"
echo.
echo Press any key here when you're finished to close the tunnel...
pause >nul
goto :cleanup

rem ===========================================================================
:cleanup
echo.
if defined SSH_PID (
    echo Closing SSH tunnel...
    taskkill /PID !SSH_PID! /T /F >nul 2>&1
)
if defined DELETE_PROFILE if exist "!PROFILE_DIR!" rmdir /s /q "!PROFILE_DIR!" >nul 2>&1
echo ============================================================================
echo  OpenClaw session closed.
echo ============================================================================
timeout /t 2 >nul
exit /b 0

rem --- Errors ----------------------------------------------------------------
:no_host
echo [ERROR] No host given.
goto :fail

:no_ssh
echo [ERROR] ssh was not found. Install the Windows "OpenSSH Client" optional feature:
echo         Settings ^> System ^> Optional features ^> Add a feature ^> OpenSSH Client
goto :fail

:ssh_start_failed
echo [ERROR] Could not start ssh.
goto :fail

:ssh_died
echo.
echo [ERROR] The SSH connection closed before the tunnel opened.
echo         Common causes: wrong password, host unreachable, SSH port blocked,
echo         or nothing listening on port !OPENCLAW_REMOTE_PORT! on the remote machine.
goto :fail

:tunnel_timeout
echo [ERROR] Gave up waiting for the tunnel after 5 minutes.
goto :fail

:fail
if defined SSH_PID taskkill /PID !SSH_PID! /T /F >nul 2>&1
echo.
pause
exit /b 1

rem --- Helpers ---------------------------------------------------------------
:port_listening
rem errorlevel 0 if something is listening on local TCP port %1, else 1.
netstat -ano | findstr /r /c:":%~1 .*LISTENING" >nul
exit /b %errorlevel%

:usage
echo OpenClaw Web UI launcher
echo.
echo Opens an SSH tunnel to a remote OpenClaw gateway that only listens on its own
echo loopback address, shows the Control UI in an app window, and closes the
echo tunnel when you close that window.
echo.
echo Usage:
echo   %~nx0 [user@]host [remote_port] [local_port]
echo.
echo   host         Remote machine running the OpenClaw gateway
echo   remote_port  Gateway port on the remote machine   (default 18789)
echo   local_port   Port to use on this PC               (default = remote_port)
echo.
echo Environment variables or openclaw_gui.config.cmd can set:
echo   OPENCLAW_HOST, OPENCLAW_USER, OPENCLAW_SSH_PORT (default 22),
echo   OPENCLAW_SSH_KEY (path to a private key), OPENCLAW_REMOTE_PORT,
echo   OPENCLAW_LOCAL_PORT, OPENCLAW_BROWSER (path to chrome.exe or msedge.exe),
echo   OPENCLAW_KEEP_PROFILE=1 (keep the browser profile so the UI stays signed in)
echo.
echo Run with no arguments and no config to be prompted.
exit /b 0
