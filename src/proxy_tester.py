import subprocess
import time
import json
import os
from io import BytesIO
from typing import Optional

import requests

from src.speedtest_helper import (
    build_requests_proxy,
    build_urllib_proxy_url,
    create_speedtest_with_proxy,
    redact_proxy_credentials,
)

from src.utils import format_latency, get_location_from_ip
from src.config import (
    IP_API_URL,
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

    # Try requests first (more reliable), fallback to curl
    proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
    
    # Method 1: Try with requests (more reliable for proxy testing)
    try:
        print_debug("Attempting connection with requests library...")
        proxies = {'http': proxy_url, 'https': proxy_url}
        
        start = time.time()
        response = requests.get(IP_API_URL, proxies=proxies, timeout=15)
        latency = time.time() - start

        if response.status_code == 200:
            data = response.json()
            print_debug(f"Raw API response: {response.text}")
            
            result.update({
                "IP": data.get("ip", "N/A"),
                "Latency": format_latency(latency),
                "Status": "Working"
            })
            
            print_debug(f"HTTP proxy test successful via requests - IP: {result['IP']}, Latency: {result['Latency']}")
            return result
            
    except Exception as e:
        print_debug(f"Requests method failed: {str(e)}")

    # Method 2: Fallback to curl with longer timeout
    curl_cmd = [
        "curl",
        "-x", proxy_url,
        IP_API_URL,
        "--max-time", "20",  # Increased timeout
        "--connect-timeout", "15",  # Connection timeout
        "--silent",
        "--show-error"
    ]

    print_debug(f"Fallback: Executing curl command with extended timeout")

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
        
        print_debug(f"HTTP proxy test successful via curl - IP: {result['IP']}, Latency: {result['Latency']}")

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

def test_socks_speed_speedtest(proxy: dict) -> Optional[float]:
    """Test SOCKS5 proxy speed using speedtest-cli (fallback method)"""
    print_debug(f"[SPEEDTEST-CLI FALLBACK] Testing SOCKS5 proxy {proxy['raw']}")
    
    try:
        st = create_speedtest_with_proxy(proxy, timeout=40, secure=False)
        best_server = st.get_best_server()
        print_debug(f"Server: {best_server['sponsor']} - {best_server['name']}")
        
        # Simple single test with default threads for fallback
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        if download_speed > 0.1:
            print_debug(f"[FALLBACK] Speedtest-cli SOCKS5: {round(download_speed, 2)} Mbps")
            return download_speed
        return None
    except Exception as e:
        print_debug(f"[ERROR] Speedtest-cli SOCKS5 fallback failed: {str(e)}")
        return None

def test_http_speed_speedtest(proxy: dict) -> Optional[float]:
    """Test HTTP proxy speed using speedtest-cli (fallback method)"""
    print_debug(f"[SPEEDTEST-CLI FALLBACK] Testing HTTP proxy {proxy['raw']}")
    
    try:
        st = create_speedtest_with_proxy(proxy, timeout=40, secure=False)
        best_server = st.get_best_server()
        print_debug(f"Server: {best_server['sponsor']} - {best_server['name']}")
        
        # Simple single test with default threads for fallback
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        if download_speed > 0.1:
            print_debug(f"[FALLBACK] Speedtest-cli HTTP: {round(download_speed, 2)} Mbps")
            return download_speed
        return None
    except Exception as e:
        print_debug(f"[ERROR] Speedtest-cli HTTP fallback failed: {str(e)}")
        return None

def test_cloudflare_speed(proxy: dict) -> Optional[float]:
    """Test speed using Cloudflare's speed test (most accurate method)"""
    print_debug(f"[CLOUDFLARE] Starting Cloudflare speed test for {proxy['raw']}")
    
    try:
        proxies = build_requests_proxy(proxy)
        
        # Fast-fail check: Download 1MB first to detect dead/slow proxies quickly
        quick_test_url = "https://speed.cloudflare.com/__down?bytes=1000000"  # 1MB
        
        print_debug(f"[CLOUDFLARE] Quick pre-check (1MB) to detect slow proxies...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'identity',
        }
        
        session = requests.Session()
        session.proxies = proxies
        
        # Quick test - if this takes > 10 seconds, proxy is too slow
        quick_start = time.time()
        try:
            response = session.get(quick_test_url, stream=True, timeout=15, headers=headers)
            response.raise_for_status()
            
            quick_downloaded = 0
            for chunk in response.iter_content(chunk_size=524288):
                if chunk:
                    quick_downloaded += len(chunk)
                if time.time() - quick_start > 10:  # 10 second timeout
                    break
            
            quick_duration = time.time() - quick_start
            
            # If we couldn't even download 1MB in 10 seconds, proxy is too slow
            if quick_downloaded < 500000 or quick_duration > 10:  # Less than 500KB or took too long
                quick_speed = (quick_downloaded * 8) / (quick_duration * 1_000_000)
                print_debug(f"[CLOUDFLARE] Quick test: {quick_speed:.2f} Mbps - proxy too slow, skipping full test")
                return quick_speed if quick_speed > 0.1 else None
            
            quick_speed = (quick_downloaded * 8) / (quick_duration * 1_000_000)
            print_debug(f"[CLOUDFLARE] Quick test passed: ~{quick_speed:.2f} Mbps - proceeding with full test")
            
        except Exception as e:
            print_debug(f"[CLOUDFLARE] Quick test failed: {str(e)[:50]} - proxy likely dead")
            return None
        
        # Full test with 100MB download
        test_url = "https://speed.cloudflare.com/__down?bytes=100000000"  # 100MB
        
        print_debug(f"[CLOUDFLARE] Full test: 100MB download for 10 seconds...")
        
        response = session.get(test_url, stream=True, timeout=30, headers=headers)
        response.raise_for_status()
        
        downloaded = 0
        start_time = time.time()
        test_duration = 10  # 10 second test for consistency
        
        # Download with 512KB chunks (optimal for proxies)
        for chunk in response.iter_content(chunk_size=524288):
            if chunk:
                downloaded += len(chunk)
                if time.time() - start_time >= test_duration:
                    break
        
        duration = time.time() - start_time
        
        if downloaded > 1024 * 1024 and duration > 0:  # At least 1MB
            speed_mbps = (downloaded * 8) / (duration * 1_000_000)
            print_debug(f"[CLOUDFLARE] Downloaded {downloaded/1024/1024:.2f} MB in {duration:.2f}s = {speed_mbps:.2f} Mbps")
            print_debug(f"[SUCCESS] Cloudflare speed test: {speed_mbps:.2f} Mbps")
            return speed_mbps
        else:
            print_debug(f"[CLOUDFLARE] Insufficient data: {downloaded/1024:.1f}KB")
            return None
            
    except Exception as e:
        print_debug(f"[ERROR] Cloudflare speed test failed: {str(e)}")
        return None

# Using Cloudflare speed test for accurate results

def run_speed_test(proxy: dict, result: dict) -> None:
    """Run speed test using Cloudflare (most accurate method)"""
    try:
        print_debug(f"Starting speed test for {proxy['raw']} (type: {proxy.get('type', 'unknown')})")
        
        # Primary method: Cloudflare speed test (proven 94.7% accuracy)
        print_debug("Using Cloudflare speed test (accurate method)...")
        speed = test_cloudflare_speed(proxy)
        
        # Fallback: Try speedtest-cli if Cloudflare fails
        if speed is None or speed < 0.5:
            print_debug("Cloudflare failed, trying speedtest-cli as fallback...")
            
            if proxy.get('type') == 'socks5':
                speed = test_socks_speed_speedtest(proxy)
            else:
                speed = test_http_speed_speedtest(proxy)
        
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