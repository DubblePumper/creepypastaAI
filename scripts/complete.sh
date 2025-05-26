#!/bin/bash
# CreepyPasta AI - Complete Workflow
# This script runs the complete workflow (scrape + audio + video)

echo
echo "====================================="
echo "  CreepyPasta AI - Complete Workflow"
echo "====================================="
echo

if [ -z "$1" ]; then
    read -p "Enter number of stories to process (default: 3): " stories
    stories=${stories:-3}
else
    stories=$1
fi

echo "Running complete workflow for $stories stories..."
echo "This will: scrape stories → generate audio → create videos"
echo

python main.py --mode complete --stories $stories --verbose

echo
echo "Complete workflow finished!"
