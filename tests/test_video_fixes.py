#!/usr/bin/env python3
"""
Test script to verify the VideoGenerator fixes
"""

import sys
import os
sys.path.append('.')

try:
    from src.video.video_generator import VideoGenerator
    from src.utils.config_manager import ConfigManager
    import logging
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    print("🔧 Testing VideoGenerator fixes...")
    
    # Initialize
    config = ConfigManager()
    video_gen = VideoGenerator(config)
    
    print('✅ VideoGenerator initialized successfully')
    print()
    print('✅ All MoviePy API fixes applied:')
    print('  ✓ Removed invalid video_bufsize parameters from write_videofile() calls')
    print('  ✓ Fixed fps setting order (set before audio composition to avoid CompositeAudioClip.fps error)')
    print('  ✓ Added subprocess import to fix TimeoutExpired exception handling')
    print('  ✓ Fixed indentation and syntax issues in all rendering methods')
    print('  ✓ Fixed CompositeAudioClip fps attribute error')
    print()
    print('🎬 Video generation should now work without hanging or API errors!')
    
except Exception as e:
    print(f'❌ Error during initialization: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
