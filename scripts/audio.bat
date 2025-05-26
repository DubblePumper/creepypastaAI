@echo off
REM CreepyPasta AI - Audio Only Mode
REM This script generates audio files for existing stories

echo.
echo =====================================
echo  CreepyPasta AI - Audio Mode
echo =====================================
echo.

echo Generating audio files for existing stories...
python main.py --mode audio --verbose

echo.
echo Audio generation completed!
echo Use 'video.bat' to generate video files from audio
pause
