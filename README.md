# Proxidize: Proxy Tester






______              _     _ _         
| ___ \            (_)   | (_)        
| |_/ / __ _____  ___  __| |_ _______ 
|  __/ '__/ _ \ \/ / |/ _` | |_  / _ \
| |  | | | (_) >  <| | (_| | |/ /  __/
\_|  |_|  \___/_/\_\_|\__,_|_/___\___|





---------------------------------------------------------------------------------------------------------------------------------                                                                            
A professional, multi-threaded proxy testing tool for HTTP and SOCKS5 proxies with built-in speed testing and geo-location lookup.
---------------------------------------------------------------------------------------------------------------------------------


## Features

- 🚀 **Multi-threaded Testing**: Efficient parallel proxy testing with intelligent thread management
- 🌍 **HTTP & SOCKS5 Support**: Test both HTTP and SOCKS5 proxies seamlessly
- 📍 **Geo-location Lookup**: Get detailed location information for working proxies
- ⚡ **Speed Testing**: Built-in download speed testing using speedtest-cli
- 🎨 **Beautiful UI**: Rich terminal interface with colored output and formatted tables
- 📊 **Export Results**: Save results to CSV format for analysis
- 🛡️ **Robust Error Handling**: Graceful handling of failures and interruptions
- 🔧 **Flexible Input**: Support for single proxy, file input, or interactive proxy entry

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

# Export results to CSV
proxidize_pt --http --geo proxies.txt -o results.csv

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

## Output

Results are displayed in a beautiful table format and can be exported to CSV:

```
                          Proxy Test Results
┏━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┓
┃ # ┃ Proxy Type ┃ IP Address     ┃ Location                          ┃ Latency ┃ Speed     ┃ Status  ┃
┡━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━┩
│ 1 │ HTTP       │ 172.56.168.96  │ Brooklyn, New York, United States │ 966ms   │ 5.03 Mbps │ Working │
│ 2 │ SOCKS5     │ 172.58.255.34  │ College Park, Maryland, US        │ 1240ms  │ 3.2 Mbps  │ Working │
└───┴────────────┴────────────────┴───────────────────────────────────┴─────────┴───────────┴─────────┘
```

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/fawaz7/Proxy-tester/wiki)
2. Search [existing issues](https://github.com/fawaz7/Proxy-tester/issues)
3. Create a [new issue](https://github.com/fawaz7/Proxy-tester/issues/new)

If you can't run `proxidize_pt` after installation:

- **With pipx**: Run `pipx ensurepath` and restart your terminal
- **With --user**: Add `~/.local/bin` (Linux/Mac) or `%APPDATA%\Python\Scripts` (Windows) to your PATH
- **With virtual environment**: Make sure the environment is activated

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/fawaz7/Proxy-tester/wiki)
2. Search [existing issues](https://github.com/fawaz7/Proxy-tester/issues)
3. Create a [new issue](https://github.com/fawaz7/Proxy-tester/issues/new)
