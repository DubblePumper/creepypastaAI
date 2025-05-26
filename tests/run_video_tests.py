#!/usr/bin/env python3
"""
Video Generation Test Runner

This script provides a comprehensive test runner for video generation functionality.
It can run both unittest-based tests and standalone tests, with proper output management.
"""

import sys
import unittest
from pathlib import Path
from datetime import datetime
import argparse

# Add the parent directory to Python path to access src
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.test_video_generation import TestVideoGeneration, run_standalone_tests


def run_unittest_suite():
    """Run the unittest-based test suite."""
    print("🧪 Running Video Generation Unit Tests")
    print("=" * 50)
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestVideoGeneration)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_all_tests():
    """Run both unittest and standalone tests."""
    print("🎬 CreepyPasta AI Video Generation - Complete Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run unittest suite
    unittest_success = run_unittest_suite()
    
    print("\n" + "=" * 60)
    
    # Run standalone tests
    standalone_success = run_standalone_tests()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS:")
    print(f"  Unit Tests:       {'PASSED' if unittest_success else 'FAILED'}")
    print(f"  Standalone Tests: {'PASSED' if standalone_success else 'FAILED'}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return unittest_success and standalone_success


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Video Generation Test Runner")
    parser.add_argument(
        "--mode", 
        choices=["unittest", "standalone", "all"], 
        default="all",
        help="Test mode to run (default: all)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "unittest":
        success = run_unittest_suite()
    elif args.mode == "standalone":
        success = run_standalone_tests()
    else:  # all
        success = run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
