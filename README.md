# Fwz_PT - Proxy Tester# Fawaz: Proxy Tester

A high-performance, multi-threaded proxy testing tool for HTTP and SOCKS5 proxies with accurate speed testing and geo-location lookup.A professional, high-performance proxy testing tool for HTTP and SOCKS5 proxies with accurate speed testing, geo-location lookup, and beautiful terminal UI.

---## ✨ Features

## Overview### Core Capabilities

Fwz_PT is a command-line tool designed for testing and validating proxy servers. It provides comprehensive proxy analysis including connectivity checks, speed measurements using Cloudflare CDN, and geographical location identification.- 🚀 **Multi-threaded Testing**: Intelligent parallel proxy testing with optimized thread management (up to 64 threads for connectivity checks)

- 🌍 **HTTP & SOCKS5 Support**: Seamless testing of both HTTP and SOCKS5 proxies

### Key Capabilities- 📍 **Geo-location Lookup**: Detailed location information for working proxies (City, Region, Country)

- ⚡ **Accurate Speed Testing**: Cloudflare CDN-based speed tests with 94%+ accuracy

- Multi-threaded proxy connectivity testing (up to 64 concurrent threads)- 🔄 **Sequential Speed Testing**: Each proxy tested individually for maximum accuracy (no bandwidth competition)

- Accurate speed testing using Cloudflare CDN infrastructure- 🎯 **Retry Logic**: Option to re-test failed proxies after initial run

- Geo-location lookup with city, region, and country details- 🎨 **Beautiful UI**: Rich terminal interface with progress bars, spinners, and color-coded results

- Support for both HTTP and SOCKS5 proxy protocols- 📊 **Multiple Export Formats**: Save results to TXT or CSV format

- Sequential speed testing for maximum accuracy- 🛡️ **Robust Error Handling**: Graceful handling of failures with clear error messages

- Comprehensive input validation with clear error reporting- ✅ **Input Validation**: Comprehensive validation of proxy formats before testing

- Retry logic for handling transient network failures

- Multiple output formats (TXT, CSV)### Advanced Features

---- **Fast-Fail Detection**: 1MB quick pre-check identifies slow/dead proxies in seconds

- **Flexible Proxy Formats**: Support for both `host:port:user:pass` and `user:pass@host:port` formats

## Features- **IPv4 & DNS Support**: Works with IP addresses and hostnames

- **Professional Output**: Clean, emoji-free output suitable for production environments

### Performance- **No Interactive Prompts**: When flags are provided, runs completely automated

- **Intelligent Threading**: Optimized thread management based on proxy count- **Graceful Shutdown**: Ctrl+C handling with immediate cleanup

- **Fast-Fail Detection**: 1MB pre-check identifies dead proxies in seconds

- **Sequential Speed Tests**: Each proxy tested individually for full bandwidth allocation## Installation

- **Cloudflare CDN Integration**: 94%+ accuracy compared to browser-based tests

### Recommended Installation (macOS)

### Compatibility

- **Dual Proxy Format Support**: `host:port:user:pass` and `user:pass@host:port````bash

- **Host Type Support**: IPv4 addresses and DNS hostnames# Install pipx via Homebrew (recommended method for macOS)

- **Platform Support**: Windows, Linux, macOSbrew install pipx

### User Experience# Install fwz_pt

- **Rich Terminal UI**: Progress bars, spinners, and color-coded outputpipx install fwz_pt

- **Professional Output**: Clean, production-ready formatting```

- **Verbose Mode**: Detailed debugging information when needed

- **Graceful Shutdown**: Ctrl+C handling with immediate cleanup### Recommended Installation (All Platforms)

---```bash

# Install pipx if you don't have it

## Installationpip install --user pipx

pipx ensurepath

### Method 1: Using pipx (Recommended)

# Install fwz_pt

pipx installs the tool in an isolated environment and makes it available globally.pipx install fwz_pt

````

```bash

# Install pipx if not already installed### Alternative Installation Methods

pip install --user pipx

#### Using pip with virtual environment:

# Ensure pipx path is configured

pipx ensurepath```bash

# Create a virtual environment

# Install fwz_ptpython3 -m venv proxy_tester_env

pipx install fwz_ptsource proxy_tester_env/bin/activate  # On Windows: proxy_tester_env\Scripts\activate

````

# Install the package

### Method 2: Using Virtual Environmentpip install fwz_pt

````

For isolated Python environment installation.

#### Using pip with user flag:

```bash

# Create virtual environment```bash

python -m venv venvpip install --user fwz_pt

````

# Activate virtual environment

# On Windows:#### System-wide installation (not recommended):

venv\Scripts\activate

# On Linux/macOS:```bash

source venv/bin/activatepip install --break-system-packages fwz_pt

```

# Install fwz_pt

pip install fwz_pt### From Source:

```

```bash

### Method 3: From Sourcegit clone https://github.com/fawaz7/Proxy-tester.git

cd Proxy-tester

For development or testing the latest changes.pip install -e .

```

````bash

# Clone the repository## Usage

git clone https://github.com/fawaz7/Proxy-tester.git

cd Proxy-tester### Command Line Interface



# Install dependenciesOnce installed, you can use the main command:

pip install -r requirements.txt

```bash

# Run directlyfwz_pt [options] <proxy_file_or_single_proxy>

python src/main.py --help```

````

### Basic Examples

---

````bash

## Usage# Test a single HTTP proxy

fwz_pt --http pg.proxi.es:20000:username:password

### Basic Syntax

# Test a single SOCKS5 proxy with geo-location

```bashfwz_pt --socks --geo pg.proxi.es:20002:username:password

fwz_pt [OPTIONS] <proxy_file_or_single_proxy>

```# Test proxies from a file with speed test and verbose output

fwz_pt --http --geo --speed-test -v proxies.txt

### Command Line Options

# Export results to CSV format

```fwz_pt --http --geo proxies.txt -o results.csv

positional arguments:

  proxy                 Single proxy or path to proxy list file# Export results to TXT format

fwz_pt --http --geo proxies.txt -o results.txt

options:

  -h, --help            Show this help message and exit# Without specifying extension (defaults to CSV)

  --socks               Use SOCKS5 proxy (required if not using --http)fwz_pt --http --geo proxies.txt -o results

  --http                Use HTTP proxy (required if not using --socks)

  --geo                 Enable IP geolocation lookup# Interactive mode (no arguments)

  --speed-test          Include download speed test using Cloudflare CDNfwz_pt

  -o OUTPUT, --output OUTPUT```

                        Output file path (.txt or .csv extension)

  -v, --verbose         Enable verbose debug output### Command Line Options

````

````

**Note**: You must specify either `--http` or `--socks` to indicate the proxy type.positional arguments:

  proxy                 Single proxy or path to proxy list file

---

options:

## Examples  -h, --help            Show this help message and exit

  --socks               Use SOCKS5 proxy (required if not using --http)

### Basic Connectivity Test  --http                Use HTTP proxy (required if not using --socks)

  --geo                 Enable IP geolocation lookup (optional)

Test HTTP proxies from a file:  --speed-test          Include download speed test using Cloudflare CDN (optional)

```bash  -o OUTPUT, --output OUTPUT

fwz_pt --http proxies.txt                        Output file path (.txt or .csv extension)

```  -v, --verbose         Enable verbose debug output

````

Test a single SOCKS5 proxy:

```bash**Important:** You must specify either `--http`or`--socks` to indicate the proxy type. The tool no longer auto-detects type based on port numbers for better reliability.

fwz_pt --socks proxy.example.com:1080:user:pass

````### Speed Testing Technology



### With Geo-LocationThe tool uses **Cloudflare CDN** for speed tests, providing:



```bash- **94%+ accuracy** compared to browser-based tests

fwz_pt --http --geo proxies.txt- **Fast-fail detection** with 1MB pre-check (identifies dead proxies in 3 seconds)

```- **Sequential testing** - each proxy tested individually for full bandwidth

- **10-second tests** with 100MB downloads for consistent measurements

### With Speed Testing- **Fallback to speedtest-cli** if Cloudflare tests fail



```bashThis approach ensures production-grade accuracy without the inconsistency of traditional speedtest-cli methods.

fwz_pt --socks --speed-test proxies.txt

```### Output Formats



### Complete Analysis with OutputResults can be saved in two formats by specifying the file extension:



```bash- **TXT format**: Use `.txt` extension (e.g., `results.txt`) - Tab-separated values, human-readable plain text format (default)

fwz_pt --http --geo --speed-test proxies.txt -o results.csv- **CSV format**: Use `.csv` extension (e.g., `results.csv`) - Comma-separated values, ideal for spreadsheet applications and data analysis

````

The output format is automatically determined by the file extension you provide. If no extension is specified, TXT format is used by default.

### Verbose Mode

### Proxy Formats

```bash

fwz_pt --http --geo --speed-test -v proxies.txtThe tool supports **two common proxy formats**:

```

**Format 1:** `host:port:username:password`

---

```

## Proxy Formatproxy.example.com:8080:user123:pass123

192.168.1.100:3128:admin:secret

### Supported Formatspg.proxi.es:20000:username:password

```

**Format 1: Colon-Separated**

```**Format 2:** `username:password@host:port`

host:port:username:password

````

user123:pass123@proxy.example.com:8080

**Format 2: At-Sign Notation**admin:secret@192.168.1.100:3128

```username:password@pg.proxi.es:20002

username:password@host:port```

```

**Supported Host Types:**

### Host Types

- ✅ IPv4 addresses (e.g., `192.168.1.1`)

- **IPv4 Address**: `192.168.1.100:8080:admin:secret`- ✅ DNS hostnames (e.g., `proxy.example.com`, `pg.proxi.es`)

- **DNS Hostname**: `proxy.example.com:3128:user:pass`

**Input Validation:**

### Example Proxy FileThe tool validates all inputs before testing:



Create a text file (e.g., `proxies.txt`) with one proxy per line:- Port must be numeric and in range 1-65535

- Host, username, and password cannot be empty

```- IPv4 addresses must have valid octets (0-255)

proxy1.example.com:8080:user1:pass1- Hostnames must follow valid DNS format

192.168.1.100:3128:admin:secret

user2:pass2@proxy2.example.com:1080Invalid proxies are skipped with clear error messages indicating the issue.

admin:secret@10.0.0.50:8080

```### Input Methods



---1. **Single Proxy**: Pass a proxy directly as an argument (without quotes)

2. **File Input**: Create a text file with one proxy per line

## Output Formats3. **Interactive Mode**: Run without arguments to enter proxies manually. After testing, you'll be prompted to save results in TXT format by default (or CSV if you specify .csv extension).



### Console Output### Example File (proxies.txt):



Results are displayed in a formatted table:```

proxy1.example.com:8080:user1:pass1

```proxy2.example.com:3128:user2:pass2

                          Proxy Test Resultspg.proxi.es:20000:username:password

┏━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┓pg.proxi.es:20002:username:password

┃ # ┃ Proxy Type ┃ IP Address     ┃ Location              ┃ Latency ┃ Speed     ┃ Status  ┃```

┡━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━┩

│ 1 │ HTTP       │ 172.56.168.96  │ New York, NY, US      │ 966ms   │ 7.02 Mbps │ Working │## Platform Support

│ 2 │ SOCKS5     │ 172.58.255.34  │ Maryland, US          │ 1240ms  │ 5.34 Mbps │ Working │

└───┴────────────┴────────────────┴───────────────────────┴─────────┴───────────┴─────────┘Fwz_PT works on all major platforms:

```

- ✅ **Windows** (Windows 10, 11)

### File Output- ✅ **Linux** (Ubuntu, Debian, CentOS, etc.)

- ✅ **macOS** (10.14+)

**TXT Format** (Tab-separated values):

```bash## Requirements

fwz_pt --http proxies.txt -o results.txt

```- Python 3.7 or higher

- Internet connection for proxy testing

**CSV Format** (Comma-separated values):- All dependencies are automatically installed via pip

```bash

fwz_pt --http proxies.txt -o results.csv## Output

```

Results are displayed in a beautiful table format with color-coded status:

---

```

## Speed Testing                          Proxy Test Results

┏━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┓

### Cloudflare CDN Technology┃ # ┃ Proxy Type ┃ IP Address     ┃ Location                          ┃ Latency ┃ Speed     ┃ Status  ┃

┡━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━┩

Fwz_PT uses Cloudflare's CDN infrastructure for speed testing, providing:│ 1 │ HTTP       │ 172.56.168.96  │ Brooklyn, New York, United States │ 966ms   │ 7.02 Mbps │ Working │

│ 2 │ SOCKS5     │ 172.58.255.34  │ College Park, Maryland, US        │ 1240ms  │ 5.34 Mbps │ Working │

- **High Accuracy**: 94%+ correlation with browser-based tests└───┴────────────┴────────────────┴───────────────────────────────────┴─────────┴───────────┴─────────┘

- **Fast Pre-Check**: 1MB download in 3 seconds identifies slow proxies```

- **Full Bandwidth Test**: 100MB download over 10 seconds for accurate measurement

- **No Throttling**: 500ms delay between tests prevents CDN rate limiting### Speed Test Progress



### Sequential Testing StrategyWhen running speed tests, you'll see a beautiful progress display:



Speed tests run sequentially (one at a time) to ensure:```

- Each proxy receives full available bandwidthSpeed Test Phase

- No competition between concurrent tests━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Consistent and reproducible results

- Professional-grade accuracyTesting 5 proxies sequentially

• Each proxy tested individually for 100% accuracy

---• Full bandwidth allocated per test

• ETA calculated in real-time

## Input Validation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The tool validates all proxy inputs before testing:

Speed testing proxies... ━━━━━━━━━━━━━━━━━━━━━ 3/5 │ 60% │ 0:00:23 │ 0:00:15

- **Port Range**: Must be between 1-65535

- **IPv4 Format**: Valid octets (0-255) if using IP address#01/05 │ 172.56.168.96  │ 7.02 Mbps │ Brooklyn, New York, US

- **Hostname Format**: Valid DNS naming convention#02/05 │ 172.58.255.34  │ 5.34 Mbps │ College Park, Maryland, US

- **Required Fields**: Host, port, username, and password must be non-empty#03/05 │ 172.59.123.45  │ 8.49 Mbps │ Seattle, Washington, US

```

Invalid proxies are skipped with clear error messages indicating the specific issue.

### Retry Failed Proxies

---

After testing completes, if any proxies failed, you'll be prompted:

## Performance

```

### Threading StrategyWould you like to test 3 failed proxies again? [y/N]:

```

- **Connectivity Tests**: Up to 64 concurrent threads (optimized based on proxy count)

- **Geo-IP Lookups**: Up to 32 concurrent threadsThis handles transient network failures without re-testing working proxies.

- **Speed Tests**: Sequential (1 at a time) for maximum accuracy

## Performance

### Retry Logic

### Threading Strategy

After testing completes, if any proxies failed, you'll be prompted:

- **Connectivity Tests**: Up to 64 concurrent threads (optimized based on proxy count)

```- **Geo-IP Lookups**: Up to 32 concurrent threads

Would you like to test 3 failed proxies again? [y/N]:- **Speed Tests**: Sequential (1 at a time) for maximum accuracy

```

### Speed Test Accuracy

This handles transient network failures without re-testing working proxies.

- **Cloudflare CDN**: 94.7% accuracy compared to browser tests

---- **Fast-fail**: Dead proxies detected in ~3 seconds (1MB pre-check)

- **Full test**: 10-second downloads (100MB) for consistent measurements

## Troubleshooting- **No throttling**: 500ms delay between tests prevents CDN rate limiting



### Installation Issues## Troubleshooting



**Error: "externally-managed-environment"**### Installation Issues



This occurs on newer Python installations. Solution:#### Error: "externally-managed-environment"



```bashThis error occurs on newer Python installations (especially with Homebrew on macOS). Use one of these solutions:

pip install --user pipx

pipx install fwz_pt1. **Recommended**: Use `pipx` for application installation:

```

   ```bash

**Command not found after installation**   pip install --user pipx

   pipx install fwz_pt

Add the appropriate directory to your PATH:   ```

- **Linux/macOS**: `~/.local/bin`

- **Windows**: `%APPDATA%\Python\Scripts`2. **Use virtual environment**:



Or use pipx:   ```bash

```bash   python3 -m venv venv

pipx ensurepath   source venv/bin/activate  # On Windows: venv\Scripts\activate

```   pip install fwz_pt

   ```

### Usage Issues

3. **User installation**:

**"Invalid proxy format" errors**   ```bash

   pip install --user fwz_pt

Ensure proxies follow one of the supported formats:   ```

- `host:port:username:password`

- `username:password@host:port`#### PATH Issues



**Speed tests failing**If you can't run `fwz_pt` after installation:



Some proxies may block Cloudflare CDN. The tool automatically falls back to speedtest-cli. Use `-v` flag to see detailed error messages.- **With pipx**: Run `pipx ensurepath` and restart your terminal

- **With --user**: Add `~/.local/bin` (Linux/Mac) or `%APPDATA%\Python\Scripts` (Windows) to your PATH

**Slow performance**- **With virtual environment**: Make sure the environment is activated



- Speed tests run sequentially by design for accuracy### Common Usage Issues

- Use `--geo` and `--speed-test` flags only when needed

- Large proxy lists benefit from the fast-fail pre-check#### "Invalid proxy format" errors



---- Ensure proxies follow one of the supported formats

- Check for typos in host, port, username, or password

## Requirements- Verify port is numeric and between 1-65535



- Python 3.7 or higher#### Speed tests failing

- Internet connection for proxy testing

- All dependencies automatically installed via pip- Some proxies may block Cloudflare CDN - this is normal

- Tool will fall back to speedtest-cli automatically

---- Use `-v` flag to see detailed error messages



## License#### Slow performance



This project is licensed under the MIT License - see the LICENSE file for details.- Reduce concurrent threads if system is overwhelmed

- Speed tests run sequentially by design (for accuracy)

---- Use `--geo` and `--speed-test` flags only when needed



## Author## What's New in v1.1.0



**Fawaz Al-Ghzawi**  ### Major Improvements

Email: Ghazawe1@gmail.com

GitHub: https://github.com/fawaz7/Proxy-tester- ✅ **Cloudflare CDN Speed Tests**: Replaced speedtest-cli with Cloudflare for 94%+ accuracy

- ✅ **Sequential Speed Testing**: Each proxy gets full bandwidth for accurate measurements

---- ✅ **Both Proxy Formats**: Support for `host:port:user:pass` and `user:pass@host:port`

- ✅ **Input Validation**: Comprehensive validation with clear error messages

## Contributing- ✅ **Retry Logic**: Option to re-test failed proxies after initial run

- ✅ **Beautiful UI**: Rich progress bars, spinners, and color-coded results

Contributions are welcome. Please feel free to submit a Pull Request.- ✅ **No Auto-Prompts**: Runs fully automated when flags are provided

- ✅ **Professional Output**: Removed emojis, clean production-ready output

## Support- ✅ **Fast-Fail Detection**: 1MB pre-check identifies slow proxies quickly



For issues or questions:### Technical Improvements

1. Search [existing issues](https://github.com/fawaz7/Proxy-tester/issues)

2. Create a [new issue](https://github.com/fawaz7/Proxy-tester/issues/new)- Optimized threading strategy (up to 64 threads for connectivity)

- Improved error handling and graceful shutdown

---- Better memory management for large proxy lists

- Enhanced verbose mode for debugging

**Version**: 1.1.0

**Last Updated**: October 27, 2025## License


This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/fawaz7/Proxy-tester/wiki)
2. Search [existing issues](https://github.com/fawaz7/Proxy-tester/issues)
3. Create a [new issue](https://github.com/fawaz7/Proxy-tester/issues/new)

## Support

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/fawaz7/Proxy-tester/wiki)
2. Search [existing issues](https://github.com/fawaz7/Proxy-tester/issues)
3. Create a [new issue](https://github.com/fawaz7/Proxy-tester/issues/new)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Made with ❤️ for the proxy testing community**
````
