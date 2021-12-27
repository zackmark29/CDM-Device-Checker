@echo off
echo.
cd /d "C:\Users\Admin\Downloads\cdm_device_checker"
set arg=%*
echo %arg%
py check.py %arg%
echo.
pause