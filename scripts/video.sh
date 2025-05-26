#!/bin/bash
# CreepyPasta AI - Video Only Mode
# This script generates video files for existing audio files

echo
echo "====================================="
echo "  CreepyPasta AI - Video Mode"
echo "====================================="
echo

echo "Choose an option:"
echo "1. Generate videos for stories without videos (default)"
echo "2. Generate videos for ALL audio files (regenerate existing)"
echo

read -p "Enter your choice (1-2, default: 1): " choice
choice=${choice:-1}

if [ "$choice" = "2" ]; then
    echo "Generating videos for ALL existing audio files..."
    python main.py --mode video --video-all --verbose
else
    echo "Generating videos for stories without videos..."
    python main.py --mode video --verbose
fi

echo
echo "Video generation completed!"
