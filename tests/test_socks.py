import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.proxy_tester import test_socks_proxy
from src.utils import parse_proxy_line
from src.ui import print_info

def test_single_socks_proxy():
    print_info("[INFO] Running SOCKS5 proxy test...\n")

    raw_proxy = "pg.proxi.es:20002:f7VPm5tW0JN1NySx-s-JgWavCRyTX:Q1GdSz9Ah4AeFYlV"
    proxy = parse_proxy_line(raw_proxy)

    result = test_socks_proxy(proxy)

    print_info(f"[{result['Status']}] {proxy['host']}:{proxy['port']}")
    print(f"  IP: {result['IP']}")
    print(f"  Location: {result['Location']}")
    print(f"  Latency: {result['Latency']}\n")

if __name__ == "__main__":
    test_single_socks_proxy()
