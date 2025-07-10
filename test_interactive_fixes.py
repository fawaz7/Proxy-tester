#!/usr/bin/env python3
"""
Test script to verify interactive prompt fixes
"""

import sys
import os
from unittest.mock import Mock

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_interactive_prompt_with_flags():
    """Test that interactive prompt respects CLI flags"""
    
    print("="*60)
    print("🧪 Testing interactive prompt with flags")
    print("="*60)
    
    from src.cli import interactive_prompt
    
    # Create mock args object with flags set
    mock_args = Mock()
    mock_args.proxy = "test.txt"
    mock_args.sock = False
    mock_args.http = True
    mock_args.geo = True  # GEO FLAG SET
    mock_args.speed_test = True  # SPEED TEST FLAG SET
    mock_args.threads = 10
    mock_args.timeout = 30
    mock_args.verbose = True  # VERBOSE FLAG SET
    mock_args.output = "results.csv"  # OUTPUT FLAG SET
    
    config = interactive_prompt(mock_args)
    
    print("🔍 Configuration generated:")
    print(f"  • geo_lookup: {config['geo_lookup']}")
    print(f"  • speed_test: {config['speed_test']}")
    print(f"  • verbose: {config['verbose']}")
    print(f"  • output_path: {config['output_path']}")
    print(f"  • type: {config['type']}")
    
    # Verify that flags were respected
    success = True
    
    if not config['geo_lookup']:
        print("❌ Geo lookup should be True when --geo flag is set")
        success = False
    else:
        print("✅ Geo lookup correctly set from flag")
        
    if not config['speed_test']:
        print("❌ Speed test should be True when --speed-test flag is set")
        success = False
    else:
        print("✅ Speed test correctly set from flag")
        
    if not config['verbose']:
        print("❌ Verbose should be True when --verbose flag is set")
        success = False
    else:
        print("✅ Verbose correctly set from flag")
        
    if config['output_path'] != "results.csv":
        print("❌ Output path should be 'results.csv' when -o flag is set")
        success = False
    else:
        print("✅ Output path correctly set from flag")
        
    if config['type'] != "http":
        print("❌ Type should be 'http' when --http flag is set")
        success = False
    else:
        print("✅ Proxy type correctly set from flag")
    
    print("\n" + "="*60)
    if success:
        print("🎉 All interactive prompt tests PASSED!")
    else:
        print("❌ Some interactive prompt tests FAILED!")
    print("="*60)

def test_interactive_prompt_without_flags():
    """Test that interactive prompt uses defaults when no flags are set"""
    
    print("\n" + "="*60)
    print("🧪 Testing interactive prompt without flags")
    print("="*60)
    
    from src.cli import interactive_prompt
    
    # Create mock args object with no flags set
    mock_args = Mock()
    mock_args.proxy = "test.txt"
    mock_args.sock = False
    mock_args.http = False
    mock_args.geo = False  # NO GEO FLAG
    mock_args.speed_test = False  # NO SPEED TEST FLAG
    mock_args.threads = 10
    mock_args.timeout = 30
    mock_args.verbose = False  # NO VERBOSE FLAG
    mock_args.output = None  # NO OUTPUT FLAG
    
    print("📝 This test would normally require interactive input.")
    print("📝 In a real scenario, the user would be prompted for:")
    print("   • Proxy type (http/socks)")
    print("   • Geo-IP lookup (y/N)")
    print("   • Speed test (y/N)")
    print("   • Output file is NOT asked (fixed!)")
    
    config = interactive_prompt(mock_args)
    
    print("\n🔍 Configuration with no flags:")
    print(f"  • output_path: {config['output_path']} (should be None)")
    print(f"  • verbose: {config['verbose']} (should be False)")
    
    if config['output_path'] is None:
        print("✅ Output path correctly set to None when no -o flag")
    else:
        print("❌ Output path should be None when no -o flag")
    
    if not config['verbose']:
        print("✅ Verbose correctly set to False when no --verbose flag")
    else:
        print("❌ Verbose should be False when no --verbose flag")

if __name__ == "__main__":
    test_interactive_prompt_with_flags()
    test_interactive_prompt_without_flags()
