import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.proxy_tester import test_socks_proxy
from src.utils import parse_proxy_line
from src.ui import print_info

def test_single_socks_proxy():
    print_info("[INFO] Running SOCKS5 proxy test...\n")

    # Example proxy for testing (replace with real proxy for actual testing)
    raw_proxy = "example.proxy.com:8080:username:password"
    proxy = parse_proxy_line(raw_proxy)

    result = test_socks_proxy(proxy)

    print_info(f"[{result['Status']}] {proxy['host']}:{proxy['port']}")
    print(f"  IP: {result['IP']}")
    print(f"  Location: {result['Location']}")
    print(f"  Latency: {result['Latency']}\n")

if __name__ == "__main__":
    test_single_socks_proxy()
