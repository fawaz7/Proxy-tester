# config.py

# ==========================
# GENERAL SETTINGS
# ==========================

APP_NAME = "Proxidize: Proxy Tester"
APP_VERSION = "1.00"

DEFAULT_THREAD_COUNT = 10
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 2

# ==========================
# PROXY TESTING ENDPOINT
# ==========================

# This endpoint returns JSON like:
# { "ip": "1.2.3.4", "country": "US", "cc": "US" }
IP_API_URL = "http://api.myip.com"  # You can change to ipinfo.io, ipapi.co, etc.

# ==========================
# COLORS (OPTIONAL THEMING)
# ==========================

from colorama import Fore

COLORS = {
    "info": Fore.CYAN,
    "success": Fore.GREEN,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
    "reset": Fore.RESET
}

# ==========================
# FILES / LOGGING
# ==========================

DEFAULT_PROXY_FILE = "data/proxies.txt"
RESULTS_DIR = "data/results/"
DEFAULT_RESULT_FILE = "proxy_results.csv"
LOG_FILE = "proxy_tester.log"

# ==========================
# HEADERS
# ==========================
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT
}
