# Fwz_PT - Proxy Tester

Fast, multi-threaded proxy testing from the command line.

## Features

- Multi-threaded proxy ping testing
- Geo-location lookup
- Sequential speed testing (Cloudflare CDN + Fast.com fallback)
- Supports HTTP and SOCKS5 proxies
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

Options:

- `--http` or `--socks` - Proxy type (required)
- `--geo` - Enable geo-location lookup
- `--speed-test` - Run download speed test
- `-o <file>` - Save results (.txt or .csv)
- `--verbose` - Debug output

Proxy formats:

- `host:port:user:pass`
- `user:pass@host:port`

## Contributing

Feel free to contribute to the repository.

```

```
