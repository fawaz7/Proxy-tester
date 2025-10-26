# config.py

# ==========================
# GENERAL SETTINGS  
# ==========================

from src import __version__

APP_NAME = "Fawaz: Proxy Tester"
APP_VERSION = __version__

REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 2

# ==========================
# PROXY TESTING ENDPOINT
# ==========================

# This endpoint returns JSON like:
# { "ip": "1.2.3.4", "country": "US", "cc": "US" }
IP_API_URL = "http://api.myip.com"

# ==========================
# SPEED TEST SETTINGS
# ==========================

# Test file URL for speed testing (100MB test file)
TEST_FILE_URL = "http://speedtest.tele2.net/100MB.zip"
SPEED_TEST_DURATION = 15  # seconds (increased for better accuracy - closer to browser tests)
SPEED_TEST_CHUNK_SIZE = 1024 * 64  # 64 KB (larger chunks for better throughput)
MIN_TEST_BYTES = 5 * 1024 * 1024  # 5 MB minimum data to download (more realistic)
MAX_SPEED_TEST_TIME = 60  # seconds
SPEED_TEST_RETRIES = 2  # number of retries for failed speed tests

# Debug/Verbose mode (controlled by -v/--verbose flag)
VERBOSE_MODE = False

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
