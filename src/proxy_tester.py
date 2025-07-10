import subprocess
import time
import json
import os
from io import BytesIO
from typing import Optional

import requests
from speedtest import Speedtest

from src.utils import format_latency, get_location_from_ip
from src.config import (
    IP_API_URL, TEST_FILE_URL, SPEED_TEST_DURATION, 
    SPEED_TEST_CHUNK_SIZE, MIN_TEST_BYTES, MAX_SPEED_TEST_TIME,
    SPEED_TEST_RETRIES
)
from src.ui import print_error, print_debug

def test_http_proxy(proxy: dict) -> dict:
    """Test HTTP proxy connectivity only (fast check)"""
    print_debug(f"Testing HTTP proxy connectivity: {proxy['raw']}")
    print_debug(f"Using API endpoint: {IP_API_URL}")
    
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

    print_debug(f"Executing curl command: {' '.join(curl_cmd[:3])} [REDACTED] {' '.join(curl_cmd[4:])}")

    try:
        start = time.time()
        output = subprocess.check_output(curl_cmd, stderr=subprocess.STDOUT)
        latency = time.time() - start

        decoded = output.decode("utf-8").strip()
        print_debug(f"Raw API response: {decoded}")
        data = json.loads(decoded)

        result.update({
            "IP": data.get("ip", "N/A"),
            "Latency": format_latency(latency),
            "Status": "Working"
        })
        
        print_debug(f"HTTP proxy test successful - IP: {result['IP']}, Latency: {result['Latency']}")

    except subprocess.CalledProcessError as e:
        error_msg = e.output.decode('utf-8').strip()
        print_debug(f"Curl command failed with error: {error_msg}")
        print_error(f"[HTTP FAIL] {proxy['raw']} → curl failed: {error_msg}")
    except json.JSONDecodeError:
        print_debug(f"Failed to parse JSON response: {decoded}")
        print_error(f"[HTTP FAIL] {proxy['raw']} → Invalid JSON response")

    return result

def test_socks_proxy(proxy: dict) -> dict:
    """Test SOCKS proxy connectivity only (fast check)"""
    print_debug(f"Testing SOCKS5 proxy connectivity: {proxy['raw']}")
    print_debug(f"Using API endpoint: {IP_API_URL}")
    
    result = {
        "Type": "SOCKS5",
        "IP": "N/A",
        "Location": "N/A",
        "Latency": "N/A",
        "Speed": "N/A",
        "Status": "Failed"
    }

    socks_proxy_url = f"socks5h://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
    proxies = {
        "http": socks_proxy_url,
        "https": socks_proxy_url
    }

    print_debug(f"Using SOCKS5 proxy URL: socks5h://[REDACTED]@{proxy['host']}:{proxy['port']}")

    try:
        start = time.time()
        response = requests.get(IP_API_URL, proxies=proxies, timeout=10)
        latency = time.time() - start

        print_debug(f"SOCKS5 response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_debug(f"Raw API response: {response.text}")
            
            result.update({
                "IP": data.get("ip", "N/A"),
                "Latency": format_latency(latency),
                "Status": "Working"
            })
            
            print_debug(f"SOCKS5 proxy test successful - IP: {result['IP']}, Latency: {result['Latency']}")

    except Exception as e:
        print_debug(f"SOCKS5 proxy test failed with error: {str(e)}")
        print_error(f"[SOCKS5 FAIL] {proxy['raw']} → {e}")

    return result

def test_http_speed_speedtest(proxy: dict) -> Optional[float]:
    """Test HTTP proxy speed using speedtest-cli (preferred method for HTTP)"""
    print_debug(f"🚀 Using speedtest-cli method for HTTP proxy {proxy['raw']}")
    proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
    
    print_debug(f"Setting proxy environment variables for speedtest-cli")
    print_debug(f"Proxy URL: http://[REDACTED]@{proxy['host']}:{proxy['port']}")

    # Set proxy environment variables for speedtest-cli
    os.environ["http_proxy"] = proxy_url
    os.environ["https_proxy"] = proxy_url

    try:
        print_debug("Initializing Speedtest client...")
        st = Speedtest()
        
        print_debug("Finding best server...")
        # Find best server with reasonable timeout
        st.get_best_server()
        print_debug(f"Selected server: {st.best['sponsor']} in {st.best['name']}")
        
        print_debug("Starting download speed test...")
        # Run download test
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        print_debug(f"Raw download speed: {download_speed} Mbps")
        
        # Validate speed is reasonable
        if download_speed > 0.1:  # Minimum 0.1 Mbps to be considered valid
            print_debug(f"✅ Speedtest-cli result: {round(download_speed, 2)} Mbps")
            return download_speed
        print_debug("⚠️ Speed too low, will retry with download method")
        return None

    except Exception as e:
        print_debug(f"❌ Speedtest-cli failed: {str(e)}")
        return None

    finally:
        # Always clean up environment variables
        print_debug("Cleaning up proxy environment variables")
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)

def test_proxy_speed_download(proxy: dict, retries: int = SPEED_TEST_RETRIES) -> float:
    """Test proxy speed by downloading a file (used for SOCKS and HTTP fallback)"""
    print_debug(f"🌐 Using file download method for {proxy.get('type', 'unknown')} proxy")
    print_debug(f"Download URL: {TEST_FILE_URL}")
    print_debug(f"Test duration: {SPEED_TEST_DURATION}s, Min bytes: {MIN_TEST_BYTES/1024/1024:.1f}MB")
    
    # Configure session with proper proxy URL
    session = requests.Session()
    if proxy.get('type') == 'socks5':
        proxy_url = f"socks5h://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
        print_debug(f"Using SOCKS5 proxy: socks5h://[REDACTED]@{proxy['host']}:{proxy['port']}")
    else:
        proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
        print_debug(f"Using HTTP proxy: http://[REDACTED]@{proxy['host']}:{proxy['port']}")
    
    proxies = {"http": proxy_url, "https": proxy_url}
    session.proxies = proxies
    
    # Configure retries and timeouts
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))

    for attempt in range(retries):
        try:
            print_debug(f"📥 Starting download test (attempt {attempt + 1}/{retries})")
            start_time = time.time()
            
            with session.get(TEST_FILE_URL, stream=True, timeout=MAX_SPEED_TEST_TIME) as r:
                r.raise_for_status()
                print_debug(f"✅ Connection established, status: {r.status_code}")
                print_debug(f"Response headers: Content-Length: {r.headers.get('content-length', 'unknown')}")
                
                content = BytesIO()
                downloaded = 0
                end_time = time.time() + SPEED_TEST_DURATION
                chunk_count = 0
                
                for chunk in r.iter_content(chunk_size=SPEED_TEST_CHUNK_SIZE):
                    if not chunk:  # filter out keep-alive chunks
                        continue
                    
                    content.write(chunk)
                    downloaded += len(chunk)
                    chunk_count += 1
                    
                    # Progress update every 100 chunks
                    if chunk_count % 100 == 0:
                        elapsed = time.time() - start_time
                        current_speed = (downloaded * 8) / elapsed / 1_000_000 if elapsed > 0 else 0
                        print_debug(f"📊 Progress: {downloaded/1024/1024:.2f}MB downloaded, current speed: {current_speed:.2f} Mbps")
                    
                    if downloaded >= MIN_TEST_BYTES and time.time() >= end_time:
                        print_debug(f"✅ Reached target: {downloaded/1024/1024:.2f}MB in {time.time() - start_time:.2f}s")
                        break
                    
                    # Safety check for maximum time
                    if time.time() - start_time > MAX_SPEED_TEST_TIME:
                        print_debug("⏰ Exceeded maximum test time")
                        break
                
                total_time = time.time() - start_time
                
                if downloaded >= MIN_TEST_BYTES:
                    mbits = (downloaded * 8) / 1_000_000  # Convert to megabits
                    speed_mbps = mbits / total_time
                    print_debug(f"✅ Download complete: {downloaded/1024/1024:.2f}MB in {total_time:.2f}s = {speed_mbps:.2f} Mbps")
                    return speed_mbps
                else:
                    print_debug(f"⚠️ Insufficient data downloaded: {downloaded/1024:.2f}KB (minimum: {MIN_TEST_BYTES/1024:.2f}KB)")
                    
        except Exception as e:
            print_debug(f"❌ Download test failed (attempt {attempt + 1}/{retries}): {str(e)}")
            if attempt < retries - 1:  # Don't sleep on last attempt
                print_debug(f"⏳ Waiting 1 second before retry...")
                time.sleep(1)  # Brief pause between retries
                
    print_debug(f"❌ All {retries} download attempts failed")
    return 0  # Return 0 if all attempts failed

def run_speed_test(proxy: dict, result: dict) -> None:
    """Run speed test using the appropriate method for each proxy type"""
    try:
        print_debug(f"Starting speed test for {proxy['raw']} (type: {proxy.get('type', 'unknown')})")
        
        speed = None
        if proxy.get('type') == 'socks5':
            # SOCKS always uses download method
            speed = test_proxy_speed_download(proxy)
        else:
            # HTTP tries speedtest-cli first, falls back to download method
            speed = test_http_speed_speedtest(proxy)
            if speed is None:
                print_debug("Falling back to file download method for HTTP proxy")
                speed = test_proxy_speed_download(proxy)
        
        if speed and speed > 0:
            result["Speed"] = f"{round(speed, 2)} Mbps"
            print_debug(f"Speed test completed successfully: {result['Speed']}")
        else:
            result["Speed"] = "Error"
            print_debug("Speed test failed to get valid results")
            
    except Exception as e:
        print_error(f"[SPEEDTEST FAIL] {proxy['raw']} → {e}")
        result["Speed"] = "Error"

def run_geo_lookup(proxy: dict, result: dict) -> None:
    """Run geo-IP lookup for a working proxy"""
    ip = result.get("IP", "")
    if ip:
        result["Location"] = get_location_from_ip(ip)
    else:
        result["Location"] = "N/A"