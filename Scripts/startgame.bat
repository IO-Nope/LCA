@echo off
REM 边狱巴士的启动路径 

set gamepath="d:\SteamLibrary\steamapps\common\Limbus Company\LimbusCompany.exe"
echo checking game path:
if exist %gamepath% (
    echo File exists: %gamepath%
) else (
    echo File does not exist: %gamepath%
    echo Please check the game path in startgame.bat!
    goto :ERRPATH
)
set "processName=LimbusCompany.exe"
set /a tries=0
set flag=0
set outtime=50
:BEGIN
start cmd /c "call :timer"
set /a tries+=1
tasklist /FI "IMAGENAME eq %processName%" 2>NUL | find /I "%processName%" >NUL
    if "%ERRORLEVEL%"=="0" (
        echo %processName% already running.
        goto :SUCCESS
    )
echo starting game...
start "" %gamepath%
:CHECK
tasklist /FI "IMAGENAME eq %processName%" 2>NUL | find /I "%processName%" >NUL
if "%ERRORLEVEL%"=="0" (        
    echo %processName% already running.
    goto :SUCCESS
)
if %flag% == 0 (
    timeout /t 2 /nobreak >nul
    goto :CHECK
)
echo timeout...
if %tries% >= 6 (
    echo game is not running after 6 tries.
    goto :FAILED
)
flag = 0
echo try to restart game...
goto :BEGIN


:FAILED
exit /b 1
:SUCCESS
exit /b 0
:ERRPATH
exit /b 2

:timer
timeout /t %outtime% /nobreak 
flag = 1

