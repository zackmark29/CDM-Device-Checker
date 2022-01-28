@echo off

:-------------------------------------
REM
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    set vbs="%temp%\getadmin.vbs"
    REM create VBS script
    echo Set UAC = CreateObject^("Shell.Application"^) > %vbs%
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> %vbs%
    
    %vbs%
    del %vbs%
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

echo.
set cwd=%~dp0
set bat_file="%cwd%check.bat"
REG ADD "HKEY_CLASSES_ROOT\*\shell\Check Client Id Blob\command" /d "%bat_file% %%1"
echo.
pause