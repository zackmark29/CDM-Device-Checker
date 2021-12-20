@echo off
echo.
:start
set /p challenge="ENTER CHALLENGE DATA/PATH: "
echo.
py check.py "%challenge%"
echo.
goto start