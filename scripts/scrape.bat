@echo off
REM CreepyPasta AI - Scraping Only Mode
REM This script runs only the Reddit scraping component

echo.
echo =====================================
echo  CreepyPasta AI - Scraping Mode
echo =====================================
echo.

if "%1"=="" (
    echo Usage: scrape.bat [number_of_stories]
    echo Example: scrape.bat 10
    echo.
    set /p stories="Enter number of stories to scrape (default: 5): "
    if "!stories!"=="" set stories=5
) else (
    set stories=%1
)

echo Scraping %stories% stories from Reddit...
python main.py --mode scrape --stories %stories% --verbose

echo.
echo Scraping completed!
echo Use 'audio.bat' to generate audio files from scraped stories
pause
