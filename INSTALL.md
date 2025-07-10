# 🚀 INSTALLATION & SETUP GUIDE

This guide will help you install and set up Proxidize: Proxy Tester on Windows, Linux, and macOS.

## Quick Installation

### Option 1: Automatic Setup (Recommended)

#### Windows

```cmd
# Run the automated installer
python setup_and_test.py

# Or use the batch file
install.bat
```

#### Linux/macOS

```bash
# Run the automated installer
python3 setup_and_test.py

# Or use the shell script
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation

#### All Platforms

```bash
# Install in development mode
pip install -e .

# Or install from PyPI (when published)
pip install proxidize
```

## Usage

After installation, you can use the tool in several ways:

### 1. Console Commands (if PATH is configured)

```bash
# Main command
proxidize [options] <proxy_file_or_single_proxy>

# Alternative commands
proxy-tester [options] <proxy_file_or_single_proxy>
pxt [options] <proxy_file_or_single_proxy>
```

### 2. Python Module (Always works)

```bash
# Using Python module directly
python -m src.main [options] <proxy_file_or_single_proxy>

# Examples
python -m src.main data/working_http_proxies.txt --http --geo
python -m src.main "proxy.example.com:8080:user:pass" --http
```

### 3. Direct Script Execution

```bash
# Run the main script directly
python src/main.py [options] <proxy_file_or_single_proxy>
```

## PATH Configuration

If console commands (`proxidize`, `proxy-tester`, `pxt`) are not working, the Scripts directory is not in your PATH.

### Windows

1. **Find your Python Scripts directory:**

   ```cmd
   python -c "import sys; import os; print(os.path.join(sys.prefix, 'Scripts'))"
   ```

2. **Add to PATH:**

   - Open System Properties → Advanced → Environment Variables
   - Edit the `PATH` variable
   - Add the Scripts directory path
   - Restart your command prompt

3. **Alternative - User Scripts directory:**
   ```cmd
   python -c "import site; print(site.USER_BASE + r'\Scripts')"
   ```

### Linux/macOS

1. **Find your Python Scripts directory:**

   ```bash
   python3 -c "import site; print(site.USER_BASE + '/bin')"
   ```

2. **Add to PATH (temporary):**

   ```bash
   export PATH="$PATH:$(python3 -c 'import site; print(site.USER_BASE + "/bin")')"
   ```

3. **Add to PATH (permanent):**

   ```bash
   # For bash
   echo 'export PATH="$PATH:$(python3 -c "import site; print(site.USER_BASE + \"/bin\")")"' >> ~/.bashrc
   source ~/.bashrc

   # For zsh
   echo 'export PATH="$PATH:$(python3 -c "import site; print(site.USER_BASE + \"/bin\")")"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Verification

Test your installation:

```bash
# Test console commands (if PATH is configured)
proxidize --help
proxy-tester --help
pxt --help

# Test Python module (always works)
python -m src.main --help

# Test with sample data
python -m src.main data/working_http_proxies.txt --http --geo -v
```

## Example Usage

```bash
# Test HTTP proxies with geo-location lookup
proxidize data/working_http_proxies.txt --http --geo

# Test SOCKS5 proxies with speed test
proxidize data/working_socks_proxies.txt --sock --speed-test

# Test single proxy
proxidize "proxy.example.com:8080:username:password" --http

# Verbose output with CSV export
proxidize data/proxies.txt --http --geo --speed-test -v -o results.csv
```

## Troubleshooting

### Common Issues

1. **"proxidize command not found"**

   - Solution: Use `python -m src.main` instead, or configure PATH

2. **"No module named 'src'"**

   - Solution: Run from the project directory, or reinstall with `pip install -e .`

3. **Permission errors during installation**

   - Solution: Use `pip install --user -e .` for user installation

4. **Import errors**
   - Solution: Install dependencies with `pip install -r requirements.txt`

### Getting Help

- Check `python -m src.main --help` for usage information
- Review the main README.md for detailed documentation
- Run `python setup_and_test.py` to verify installation

## Building for Distribution

```bash
# Install build tools
pip install build twine wheel

# Build package
python -m build

# The built packages will be in dist/
# - proxidize-1.0.0.tar.gz (source distribution)
# - proxidize-1.0.0-py3-none-any.whl (wheel)
```

## Platform-Specific Notes

### Windows

- Requires Python 3.7+ with pip
- Scripts are installed in `%USERPROFILE%\AppData\Roaming\Python\Python3X\Scripts`
- Consider using PowerShell for better command support

### Linux

- Requires Python 3.7+ with pip
- Scripts are installed in `~/.local/bin`
- May need to install `python3-pip` on some distributions

### macOS

- Requires Python 3.7+ with pip
- Scripts are installed in `~/Library/Python/3.X/bin`
- Consider using Homebrew Python for easier PATH management

---

**🎉 You're all set! Enjoy using Proxidize: Proxy Tester!**
