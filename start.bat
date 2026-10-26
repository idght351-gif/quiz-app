@echo off
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo Quiz server is starting... Keep this window open while playing.
echo Host screen:  http://localhost:8080/host
echo.
%PY% quiz_game.py
pause
