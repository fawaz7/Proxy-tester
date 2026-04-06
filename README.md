# Fwz_PT - Proxy Tester

Fast, multi-threaded proxy testing from the command line.

## Features

- Multi-threaded HTTP and SOCKS5 proxy testing
- IP-whitelisted proxy support (no credentials required)
- Geo-location lookup
- Sequential speed testing (Cloudflare CDN + Fast.com fallback)
- Export results to TXT or CSV

## Installation

Recommended:

```bash
pipx install fwz-pt
```

Alternative (virtual environment):

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fwz-pt
```

From source:

```bash
git clone https://github.com/fawaz7/Proxy-tester.git
cd Proxy-tester
pip install -r requirements.txt
python src/main.py --help
```

## Usage

Basic syntax:

```bash
fwz_pt --http proxies.txt
fwz_pt --socks --geo --speed-test proxies.txt -o results.csv
```

IP-whitelisted proxies (no username/password):

```bash
fwz_pt --http --ip-whitelist proxies.txt
fwz_pt --socks --ip-whitelist 1.2.3.4:8080
```

Options:

| Flag | Description |
|------|-------------|
| `--http` | Use HTTP proxies |
| `--socks` | Use SOCKS5 proxies |
| `--ip-whitelist` | Accept `host:port` format (no credentials) |
| `--geo` | Enable geo-location lookup |
| `--speed-test` | Run download speed test |
| `-o <file>` | Save results (`.txt` or `.csv`) |
| `-v` / `--verbose` | Show debug output |

## Proxy formats

Standard (with credentials):

```
host:port:username:password
username:password@host:port
```

IP-whitelisted (with `--ip-whitelist`):

```
host:port
```

## Contributing

Feel free to open issues or pull requests on [GitHub](https://github.com/fawaz7/Proxy-tester).
