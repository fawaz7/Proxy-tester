import subprocess
import time
import json
import os
import requests
from speedtest import Speedtest, ConfigRetrievalError

from src.utils import format_latency, get_location_from_ip
from src.config import IP_API_URL
from src.ui import print_error


def test_http_proxy(proxy: dict) -> dict:
    result = {
        "Type": "HTTP",
        "IP": "N/A",
        "Location": "N/A",
        "Latency": "N/A",
        "Speed": "N/A",
        "Status": "Failed"
    }

    proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
    curl_cmd = [
        "curl",
        "-x", proxy_url,
        IP_API_URL,
        "--max-time", "10",
        "--silent",
        "--show-error"
    ]

    try:
        start = time.time()
        output = subprocess.check_output(curl_cmd, stderr=subprocess.STDOUT)
        latency = time.time() - start

        decoded = output.decode("utf-8").strip()
        data = json.loads(decoded)

        result.update({
            "IP": data.get("ip", "N/A"),
            "Location": get_location_from_ip(data.get("ip", "")) if proxy.get("geo_lookup") else "N/A",
            "Latency": format_latency(latency),
            "Status": "Working"
        })

        if proxy.get("speed_test"):
            os.environ["http_proxy"] = proxy_url
            os.environ["https_proxy"] = proxy_url

            try:
                st = Speedtest()
                st.get_best_server()
                download_speed = st.download()
                result["Speed"] = f"{round(download_speed / 1_000_000, 2)} Mbps"
            except ConfigRetrievalError:
                result["Speed"] = "Unavailable"
            except Exception as e:
                print_error(f"[SPEEDTEST FAIL] {proxy['raw']} → {e}")
                result["Speed"] = "Error"
            finally:
                os.environ.pop("http_proxy", None)
                os.environ.pop("https_proxy", None)

    except subprocess.CalledProcessError as e:
        print_error(f"[HTTP FAIL] {proxy['raw']} → curl failed: {e.output.decode('utf-8').strip()}")
    except json.JSONDecodeError:
        print_error(f"[HTTP FAIL] {proxy['raw']} → Invalid JSON response")

    return result


def test_socks_proxy(proxy: dict) -> dict:
    result = {
        "Type": "SOCKS5",
        "IP": "N/A",
        "Location": "N/A",
        "Latency": "N/A",
        "Speed": "N/A",
        "Status": "Failed"
    }

    socks_proxy_url = f"socks5://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
    proxies = {
        "http": socks_proxy_url,
        "https": socks_proxy_url
    }

    try:
        start = time.time()
        response = requests.get(IP_API_URL, proxies=proxies, timeout=10)
        latency = time.time() - start

        if response.status_code == 200:
            data = response.json()
            result.update({
                "IP": data.get("ip", "N/A"),
                "Location": get_location_from_ip(data.get("ip", "")) if proxy.get("geo_lookup") else "N/A",
                "Latency": format_latency(latency),
                "Status": "Working"
            })

            if proxy.get("speed_test"):
                result["Speed"] = "Not supported"
                print_error(f"[SPEEDTEST] SOCKS proxies are not supported for speed test via speedtest-cli")

    except Exception as e:
        print_error(f"[SOCKS5 FAIL] {proxy['raw']} → {e}")

    return result
