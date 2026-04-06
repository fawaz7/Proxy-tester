# test_utils.py
import sys
import os
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import (
    load_proxies_from_file,
    parse_proxy_line,
    format_latency,
    save_results_to_file,
    save_results_as_csv,
    save_results_as_txt,
)


sample_proxies = [
    "example.proxy.com:8080:username:password",
    "66.42.83.203:20002:user123:pass123",
    "username:password@example.proxy.com:8080",
]

sample_results = [
    {"Type": "HTTP", "IP": "1.2.3.4", "Location": "Dallas, TX", "Latency": "150ms", "Speed": "N/A", "Status": "Working"},
    {"Type": "SOCKS5", "IP": "5.6.7.8", "Location": "New York, NY", "Latency": "230ms", "Speed": "N/A", "Status": "Working"},
]


def test_proxy_validation_valid():
    for proxy in sample_proxies:
        result = parse_proxy_line(proxy)
        assert result is not None
        assert result["host"]
        assert result["port"]
        assert result["username"]
        assert result["password"]


def test_proxy_validation_invalid_format():
    try:
        parse_proxy_line("invalid:format:only")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_proxy_validation_non_numeric_port():
    try:
        parse_proxy_line("google.com:abcd:user:pass")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_proxy_validation_port_out_of_range():
    try:
        parse_proxy_line("google.com:99999:user:pass")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_parse_proxy_line_host_port_format():
    parsed = parse_proxy_line("example.proxy.com:8080:username:password")
    assert parsed["host"] == "example.proxy.com"
    assert parsed["port"] == "8080"
    assert parsed["username"] == "username"
    assert parsed["password"] == "password"


def test_parse_proxy_line_at_format():
    parsed = parse_proxy_line("username:password@example.proxy.com:8080")
    assert parsed["host"] == "example.proxy.com"
    assert parsed["port"] == "8080"
    assert parsed["username"] == "username"
    assert parsed["password"] == "password"


def test_parse_proxy_line_ip_whitelist():
    parsed = parse_proxy_line("1.2.3.4:8080", ip_whitelist=True)
    assert parsed["host"] == "1.2.3.4"
    assert parsed["port"] == "8080"
    assert parsed["username"] == ""
    assert parsed["password"] == ""


def test_parse_proxy_line_ip_whitelist_rejects_no_port():
    try:
        parse_proxy_line("1.2.3.4", ip_whitelist=True)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_format_latency():
    assert format_latency(0.321) == "321ms"
    assert format_latency(1.0) == "1000ms"
    assert format_latency(0.0) == "0ms"


def test_load_proxies_missing_file():
    proxies = load_proxies_from_file("nonexistent_file_xyz.txt")
    assert proxies == []


def test_save_results_as_csv():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode='w') as f:
        filepath = f.name
    try:
        save_results_as_csv(sample_results, filepath)
        assert os.path.exists(filepath)
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert "HTTP" in content
        assert "1.2.3.4" in content
    finally:
        os.unlink(filepath)


def test_save_results_as_txt():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode='w') as f:
        filepath = f.name
    try:
        save_results_as_txt(sample_results, filepath)
        assert os.path.exists(filepath)
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert "HTTP" in content
        assert "1.2.3.4" in content
    finally:
        os.unlink(filepath)


def test_save_results_to_file_adds_txt_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "results")
        save_results_to_file(sample_results, filepath)
        assert os.path.exists(filepath + ".txt")


if __name__ == "__main__":
    test_proxy_validation_valid()
    test_proxy_validation_invalid_format()
    test_proxy_validation_non_numeric_port()
    test_proxy_validation_port_out_of_range()
    test_parse_proxy_line_host_port_format()
    test_parse_proxy_line_at_format()
    test_parse_proxy_line_ip_whitelist()
    test_parse_proxy_line_ip_whitelist_rejects_no_port()
    test_format_latency()
    test_load_proxies_missing_file()
    test_save_results_as_csv()
    test_save_results_as_txt()
    test_save_results_to_file_adds_txt_extension()
    print("All tests passed.")
