import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui import print_banner, print_info, print_success, print_warning, print_error, display_result_table

print_banner()
print_info("Loading proxies...")
print_success("Proxy loaded successfully.")
print_warning("One proxy timed out.")
print_error("Invalid proxy format.")

sample_results = [
    {"Type": "HTTP", "IP": "23.45.67.89:8080", "Location": "Dallas, TX", "Latency": "110ms", "Status": "Working"},
    {"Type": "SOCKS", "IP": "98.76.54.32:1080", "Location": "Seattle, WA", "Latency": "250ms", "Status": "Working"},
    {"Type": "HTTP", "IP": "192.168.0.1:8000", "Location": "Unknown", "Latency": "-", "Status": "Failed"},
]

display_result_table(sample_results)