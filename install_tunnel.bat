@echo off
echo Installing cloudflared (internet tunnel tool) ...
winget install --id Cloudflare.cloudflared --source winget --accept-source-agreements --accept-package-agreements
echo.
echo Done! Now double-click start_internet.bat
pause
