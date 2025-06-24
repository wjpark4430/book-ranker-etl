@echo off
echo [INFO] Script started: %date% %time%
cd /d %~dp0

"C:\Program Files\Git\usr\bin\bash.exe" -l -c "./daily_rank.sh"

echo [INFO] Script ended: %date% %time%
pause