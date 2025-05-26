@echo off
REM CreepyPasta AI - Status and Information
REM This script displays system info and statistics

echo.
echo =====================================
echo  CreepyPasta AI - System Status
echo =====================================
echo.

echo Displaying system information...
python main.py --info

echo.
echo =====================================
echo.

echo Displaying tracking statistics...
python main.py --stats

echo.
pause
