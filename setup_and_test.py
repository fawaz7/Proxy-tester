#!/usr/bin/env python3
"""
Quick setup and test script for Proxidize
This script helps users quickly set up and test the installation
"""

import sys
import os
import subprocess
import platform

def run_command(cmd, capture_output=True, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout or "", e.stderr or ""
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Python 3.7 or higher is required")
        return False

def check_pip():
    """Check if pip is available"""
    success, stdout, stderr = run_command(f"{sys.executable} -m pip --version")
    if success:
        print(f"✅ pip is available: {stdout.strip()}")
        return True
    else:
        print("❌ pip is not available")
        return False

def install_package():
    """Install the package"""
    print("📦 Installing Proxidize...")
    
    # First upgrade pip and setuptools
    print("   Upgrading pip and setuptools...")
    success, stdout, stderr = run_command(
        f"{sys.executable} -m pip install --upgrade pip setuptools wheel"
    )
    if not success:
        print("   ⚠️ Warning: Could not upgrade pip tools")
    
    # Install in editable mode
    print("   Installing package in development mode...")
    success, stdout, stderr = run_command(
        f"{sys.executable} -m pip install -e ."
    )
    
    if success:
        print("✅ Installation completed successfully")
        return True
    else:
        print("❌ Installation failed")
        print(f"   Error: {stderr}")
        return False

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    # Test import
    try:
        import src.main
        print("✅ Package import successful")
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False
    
    # Test command-line access
    commands_to_test = ["proxidize", "proxy-tester", "pxt"]
    working_commands = []
    
    for cmd in commands_to_test:
        success, stdout, stderr = run_command(f"{cmd} --help")
        if success:
            print(f"✅ Command '{cmd}' is working")
            working_commands.append(cmd)
        else:
            print(f"❌ Command '{cmd}' is not available")
    
    return len(working_commands) > 0

def run_quick_test():
    """Run a quick functionality test"""
    print("🚀 Running quick functionality test...")
    
    try:
        # Test proxy parsing
        from src.utils import parse_proxy_line
        test_proxy = parse_proxy_line("test.example.com:8080:user:pass")
        if test_proxy and test_proxy.get('host') == 'test.example.com':
            print("✅ Proxy parsing works correctly")
        else:
            print("❌ Proxy parsing test failed")
            return False
        
        # Test thread calculation
        from src.main import calculate_optimal_threads
        threads = calculate_optimal_threads(10)
        if isinstance(threads, int) and 1 <= threads <= 64:
            print(f"✅ Thread calculation works correctly (10 proxies → {threads} threads)")
        else:
            print("❌ Thread calculation test failed")
            return False
        
        # Test UI components
        from src.ui import print_info
        print("✅ UI components are working")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main setup and test function"""
    print("=" * 60)
    print("    Proxidize: Proxy Tester - Setup & Test Script")
    print("=" * 60)
    print()
    
    # Detect platform
    system = platform.system()
    print(f"🖥️  Platform: {system} {platform.release()}")
    print()
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    if not check_python_version():
        return 1
    
    if not check_pip():
        return 1
    
    print()
    
    # Install package
    if not install_package():
        return 1
    
    print()
    
    # Test installation
    if not test_installation():
        print("⚠️ Installation completed but commands are not available in PATH")
        print("   You can still run the tool using: python -m src.main")
    
    print()
    
    # Run functionality test
    if not run_quick_test():
        print("⚠️ Some functionality tests failed")
        print("   The basic installation should still work")
    
    print()
    print("=" * 60)
    print("🎉 Setup completed!")
    print()
    print("Quick start commands:")
    print("  proxidize --help")
    print("  proxidize data/working_http_proxies.txt --http")
    print("  python -m src.main --help  # Alternative if commands not in PATH")
    print()
    print("For detailed usage instructions, see README.md")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
