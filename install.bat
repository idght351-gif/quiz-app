@echo off
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo [1/1] Installing nicegui, openpyxl, segno ...
%PY% -m pip install --upgrade -r requirements.txt
echo.
echo Done! Now double-click start.bat
pause
