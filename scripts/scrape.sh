#!/bin/bash
# CreepyPasta AI - Scraping Only Mode
# This script runs only the Reddit scraping component

echo
echo "====================================="
echo "  CreepyPasta AI - Scraping Mode"
echo "====================================="
echo

if [ -z "$1" ]; then
    read -p "Enter number of stories to scrape (default: 5): " stories
    stories=${stories:-5}
else
    stories=$1
fi

echo "Scraping $stories stories from Reddit..."
python main.py --mode scrape --stories $stories --verbose

echo
echo "Scraping completed!"
echo "Use './audio.sh' to generate audio files from scraped stories"
