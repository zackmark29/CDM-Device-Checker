@echo off
echo.
set cwd=%~dp0
cd /d %cwd%
set arg=%*
py check.py %arg%
echo.
pause