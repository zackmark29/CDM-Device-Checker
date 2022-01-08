@echo off
echo.
set cwd=%~dp0
set bat_file="%cwd%check.bat"
REG ADD "HKEY_CLASSES_ROOT\*\shell\Check Client Id Blob\command" /d "%bat_file% %%1"
echo.
pause