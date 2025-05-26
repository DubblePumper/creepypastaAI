@echo off
REM CreepyPasta AI - Complete Workflow
REM This script runs the complete workflow (scrape + audio + video)

echo.
echo =====================================
echo  CreepyPasta AI - Complete Workflow
echo =====================================
echo.

if "%1"=="" (
    set /p stories="Enter number of stories to process (default: 3): "
    if "!stories!"=="" set stories=3
) else (
    set stories=%1
)

echo Running complete workflow for %stories% stories...
echo This will: scrape stories → generate audio → create videos
echo.

python main.py --mode complete --stories %stories% --verbose

echo.
echo Complete workflow finished!
pause
