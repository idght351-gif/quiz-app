@echo off
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo Starting quiz + internet tunnel ... Keep this window open while playing.
%PY% tunnel.py
pause
