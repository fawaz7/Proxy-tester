# Proxidize: Proxy Tester - Installation Guide

This guide provides detailed installation instructions for Proxidize: Proxy Tester on all platforms.

## Installation

### Recommended Installation (macOS)

```bash
# Install pipx via Homebrew (recommended method for macOS)
brew install pipx

# Install proxidize_pt
pipx install proxidize_pt
```

### Recommended Installation (All Platforms)

```bash
# Install pipx if you don't have it
pip install --user pipx
pipx ensurepath

# Install proxidize_pt
pipx install proxidize_pt
```

### Alternative Installation Methods

#### Using pip with virtual environment:

```bash
# Create a virtual environment
python3 -m venv proxy_tester_env
source proxy_tester_env/bin/activate  # On Windows: proxy_tester_env\Scripts\activate

# Install the package
pip install proxidize_pt
```

#### Using pip with user flag:

```bash
pip install --user proxidize_pt
```

#### System-wide installation (not recommended):

```bash
pip install --break-system-packages proxidize_pt
```

### From Source:

```bash
git clone https://github.com/fawaz7/Proxy-tester.git
cd Proxy-tester
pip install -e .
```

## Usage

### Command Line Interface

Once installed, you can use the main command:

```bash
proxidize_pt [options] <proxy_file_or_single_proxy>
```

### Basic Examples

```bash
# Test a single HTTP proxy
proxidize_pt --http pg.proxi.es:20000:username:password

# Test a single SOCKS5 proxy with geo-location
proxidize_pt --socks --geo pg.proxi.es:20002:username:password

# Test proxies from a file with speed test and verbose output
proxidize_pt --http --geo --speed-test -v proxies.txt

# Export results to CSV format
proxidize_pt --http --geo proxies.txt -o results.csv

# Export results to TXT format
proxidize_pt --http --geo proxies.txt -o results.txt

# Interactive mode (no arguments)
proxidize_pt
```

### Command Line Options

```
positional arguments:
  proxy                 Single proxy or path to proxy list file

options:
  -h, --help            show this help message and exit
  --socks               Use SOCKS5 proxy
  --http                Use HTTP proxy
  --geo                 Enable IP geolocation lookup
  --speed-test          Include download speed test
  -o OUTPUT, --output OUTPUT
                        Output file path (supports .csv and .txt formats)
  -v, --verbose         Enable verbose debug output
  --speed-test          Include download speed test
  -o OUTPUT, --output OUTPUT
                        Output file path
  -v, --verbose         Enable verbose debug output
```

### Proxy Format

Proxies should be in the format: `host:port:username:password`

Examples:

```
proxy.example.com:8080:user123:pass123
192.168.1.100:3128:admin:secret
pg.proxi.es:20000:username:password
pg.proxi.es:20002:username:password
```

### Input Methods

1. **Single Proxy**: Pass a proxy directly as an argument (without quotes)
2. **File Input**: Create a text file with one proxy per line
3. **Interactive Mode**: Run without arguments to enter proxies manually

### Example File (proxies.txt):

```
proxy1.example.com:8080:user1:pass1
proxy2.example.com:3128:user2:pass2
pg.proxi.es:20000:username:password
pg.proxi.es:20002:username:password
```

## Platform Support

Proxidize works on all major platforms:

- ✅ **Windows** (Windows 10, 11)
- ✅ **Linux** (Ubuntu, Debian, CentOS, etc.)
- ✅ **macOS** (10.14+)

## Requirements

- Python 3.7 or higher
- Internet connection for proxy testing
- All dependencies are automatically installed via pip

## Troubleshooting Installation

### Error: "externally-managed-environment"

This error occurs on newer Python installations (especially with Homebrew on macOS). Use one of these solutions:

1. **Recommended**: Use `pipx` for application installation:

   ```bash
   pip install --user pipx
   pipx install proxidize_pt
   ```

2. **Use virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install proxidize_pt
   ```

3. **User installation**:
   ```bash
   pip install --user proxidize_pt
   ```

### PATH Issues

If you can't run `proxidize_pt` after installation:

- **With pipx**: Run `pipx ensurepath` and restart your terminal
- **With --user**: Add `~/.local/bin` (Linux/Mac) or `%APPDATA%\Python\Scripts` (Windows) to your PATH
- **With virtual environment**: Make sure the environment is activated

### Common Installation Issues

1. **"proxidize_pt command not found"**

   - Solution: Check PATH configuration or use `python -m proxidize_pt` instead

2. **Permission errors during installation**

   - Solution: Use `--user` flag or virtual environment instead of system-wide installation

3. **Import errors**
   - Solution: Ensure all dependencies are installed; try reinstalling with `pip install --force-reinstall proxidize_pt`

### Verification

Test your installation:

```bash
# Check version
proxidize_pt --help

# Test with a single proxy
proxidize_pt --http --geo proxy.example.com:8080:user:pass

# Test interactive mode
proxidize_pt
```

## Platform-Specific Notes

### Windows

- Requires Python 3.7+ with pip
- Use PowerShell or Command Prompt
- PATH: `%APPDATA%\Python\Scripts` (for --user installations)

### Linux

- Requires Python 3.7+ with pip
- PATH: `~/.local/bin` (for --user installations)
- May need to install `python3-pip` on some distributions

### macOS

- Requires Python 3.7+ with pip
- PATH: `~/Library/Python/3.X/bin` (for --user installations)
- Homebrew + pipx is the recommended installation method

---

**🎉 You're all set! Enjoy using Proxidize: Proxy Tester!**
