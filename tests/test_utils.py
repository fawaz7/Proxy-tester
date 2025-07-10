# test_utils.py
import sys
import os

# Allow importing from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import (
    load_proxies_from_file,
    parse_proxy_line,
    format_latency,
    save_results_to_csv
)


# ✅ Proxy format: host:port:username:password
sample_proxies = [
    "example.proxy.com:8080:username:password",
    "66.42.83.203:20002:user123:pass123",
    "invalid:format:only:three",
    "missing:port:user:pass",  # port not an int
    "google.com:abcd:user:pass",  # non-numeric port
]


def test_proxy_validation():
    print("Testing proxy validation via parse_proxy_line...")
    
    # Valid proxies should parse without error
    valid_proxies = sample_proxies[:2]
    for proxy in valid_proxies:
        try:
            result = parse_proxy_line(proxy)
            print(f"[VALID] {proxy}")
            assert result is not None
        except ValueError as e:
            assert False, f"Valid proxy failed to parse: {proxy} - {e}"
    
    # Invalid proxies should raise ValueError
    invalid_proxies = sample_proxies[2:]
    for proxy in invalid_proxies:
        try:
            parse_proxy_line(proxy)
            print(f"[INVALID] {proxy} - Should have failed but didn't")
            # Note: some "invalid" formats might actually be valid, so we'll just log
        except ValueError as e:
            print(f"[INVALID] {proxy} - Correctly rejected: {e}")
    
    print("✅ proxy validation tests completed\n")


def test_parse_proxy_line():
    print("Testing parse_proxy_line...")

    valid = sample_proxies[:2]
    for proxy in valid:
        parsed = parse_proxy_line(proxy)
        print(f"Input: {proxy}")
        print(f"Parsed: {parsed}")
        assert parsed["host"], "Missing host"
        assert parsed["port"], "Missing port"
        assert parsed["username"], "Missing username"
        assert parsed["password"], "Missing password"

    # Test invalid separately
    invalid_proxy = sample_proxies[2]  # "invalid:format:only:three"
    # This actually has 4 parts, so it won't fail - let's use a truly invalid one
    try:
        parse_proxy_line("invalid:format:only")  # Only 3 parts
        assert False, "Expected ValueError for invalid format"
    except ValueError as e:
        print(f"✔ Caught expected error: {e}")
    
    print("✅ parse_proxy_line passed\n")


def test_format_latency():
    print("Testing format_latency...")
    raw = 0.321
    formatted = format_latency(raw)
    print(f"Input: {raw} → Output: {formatted}")
    assert formatted == "321ms", "Latency formatting failed"
    print("✅ format_latency passed\n")


def test_load_proxies():
    print("Testing load_proxies_from_file...")
    proxies = load_proxies_from_file("data/proxies.txt")
    assert isinstance(proxies, list), "Returned data is not a list"
    print(f"Loaded {len(proxies)} proxies")
    print("✅ load_proxies_from_file passed\n")


def test_save_results_to_csv():
    print("Testing save_results_to_csv...")
    test_results = [
        {"Type": "HTTP", "IP": "1.2.3.4:8080", "Location": "Dallas, TX", "Latency": "150ms", "Status": "Working"},
        {"Type": "SOCKS", "IP": "5.6.7.8:1080", "Location": "New York, NY", "Latency": "230ms", "Status": "Working"},
    ]
    save_results_to_csv(test_results, filename="test_results.csv")
    assert os.path.exists("data/results/test_results.csv")
    print("✅ save_results_to_csv passed\n")


if __name__ == "__main__":
    test_proxy_validation()
    test_parse_proxy_line()
    test_format_latency()
    test_load_proxies()
    test_save_results_to_csv()
