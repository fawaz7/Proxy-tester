#!/bin/bash
# install.sh - Cross-platform installation script for Unix-like systems

set -e

echo "🚀 Installing Proxidize: Proxy Tester..."
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Error: Python 3.7+ is required but not found."
        echo "Please install Python 3.7 or higher and try again."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "📋 Detected Python version: $PYTHON_VERSION"

# Verify Python version is 3.7+
if ! $PYTHON_CMD -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
    echo "❌ Error: Python 3.7 or higher is required."
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ Error: pip is not available."
    echo "Please install pip and try again."
    exit 1
fi

echo "✅ Python and pip are available"

# Upgrade pip, setuptools, and wheel
echo "📦 Upgrading pip, setuptools, and wheel..."
$PYTHON_CMD -m pip install --upgrade pip setuptools wheel

# Install the package in development mode
echo "🔧 Installing Proxidize in development mode..."
$PYTHON_CMD -m pip install -e .

# Verify installation
echo "🧪 Verifying installation..."
if command -v proxidize &> /dev/null; then
    echo "✅ Installation successful!"
    echo ""
    echo "🎉 Proxidize is now installed and ready to use!"
    echo ""
    echo "Usage examples:"
    echo "  proxidize --help"
    echo "  proxidize data/working_http_proxies.txt --http --geo"
    echo "  proxy-tester data/working_socks_proxies.txt --socks --speed-test"
    echo "  pxt \"proxy.example.com:8080:user:pass\" --http"
    echo ""
    echo "For more information, see: README.md"
else
    echo "❌ Installation verification failed."
    echo "The 'proxidize' command is not available in PATH."
    echo "You may need to restart your terminal or check your Python PATH configuration."
    exit 1
fi
