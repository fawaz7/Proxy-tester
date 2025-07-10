#!/usr/bin/env python3
"""
Test script to verify CLI fixes
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_cli_flags():
    """Test that CLI flags work correctly"""
    
    # Test 1: Speed test flag
    print("="*60)
    print("🧪 TEST 1: Testing --speed-test flag")
    print("="*60)
    
    # Simulate arguments with speed-test flag
    original_argv = sys.argv.copy()
    sys.argv = ['test_cli.py', '--speed-test', '--http']
    
    try:
        from src.cli import parse_cli_args, interactive_prompt
        
        args = parse_cli_args()
        
        print(f"✅ args.speed_test = {args.speed_test}")
        
        if args.speed_test:
            print("✅ Speed test flag detected correctly!")
        else:
            print("❌ Speed test flag not detected!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        sys.argv = original_argv
    
    # Test 2: Geo flag
    print("\n" + "="*60)
    print("🧪 TEST 2: Testing --geo flag")
    print("="*60)
    
    sys.argv = ['test_cli.py', '--geo', '--http']
    
    try:
        args = parse_cli_args()
        
        print(f"✅ args.geo = {args.geo}")
        
        if args.geo:
            print("✅ Geo flag detected correctly!")
        else:
            print("❌ Geo flag not detected!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        sys.argv = original_argv
    
    # Test 3: Verbose flag
    print("\n" + "="*60)
    print("🧪 TEST 3: Testing --verbose flag")
    print("="*60)
    
    sys.argv = ['test_cli.py', '--verbose', '--http']
    
    try:
        args = parse_cli_args()
        
        print(f"✅ args.verbose = {args.verbose}")
        
        if args.verbose:
            print("✅ Verbose flag detected correctly!")
        else:
            print("❌ Verbose flag not detected!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        sys.argv = original_argv
    
    # Test 4: Output flag
    print("\n" + "="*60)
    print("🧪 TEST 4: Testing -o/--output flag")
    print("="*60)
    
    sys.argv = ['test_cli.py', '--output', 'test_results.csv', '--http']
    
    try:
        args = parse_cli_args()
        
        print(f"✅ args.output = {args.output}")
        
        if args.output == 'test_results.csv':
            print("✅ Output flag detected correctly!")
        else:
            print("❌ Output flag not detected correctly!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        sys.argv = original_argv

    print("\n" + "="*60)
    print("🎉 CLI flag tests completed!")
    print("="*60)

if __name__ == "__main__":
    test_cli_flags()
