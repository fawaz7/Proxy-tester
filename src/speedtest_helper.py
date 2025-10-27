"""Utility helpers for Fast.com speed testing through proxies."""
from __future__ import annotations

import time
import requests
from typing import Dict, Optional


def build_requests_proxy(proxy: dict) -> Dict[str, str]:
    """Return a requests-compatible proxy mapping for the given proxy dict."""
    scheme = "socks5h" if proxy.get("type") == "socks5" else "http"
    proxy_url = _format_proxy_url(proxy, scheme)
    return {"http": proxy_url, "https": proxy_url}


def test_fast_com_speed(proxy: dict, timeout: int = 30) -> Optional[float]:
    """
    Test download speed using Fast.com API.
    Returns speed in Mbps or None if test fails.
    
    Fast.com uses Netflix's CDN servers for accurate speed testing.
    """
    try:
        proxies = build_requests_proxy(proxy)
        
        # Step 1: Get Fast.com token
        token_url = "https://fast.com/app-ed402d.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        response = requests.get(token_url, proxies=proxies, headers=headers, timeout=timeout)
        if response.status_code != 200:
            return None
            
        # Extract token from JavaScript
        content = response.text
        token_start = content.find('token:"') + 7
        if token_start < 7:
            return None
        token_end = content.find('"', token_start)
        token = content[token_start:token_end]
        
        # Step 2: Get target URLs from Fast.com API
        api_url = f"https://api.fast.com/netflix/speedtest/v2?https=true&token={token}&urlCount=5"
        response = requests.get(api_url, proxies=proxies, headers=headers, timeout=timeout)
        if response.status_code != 200:
            return None
            
        data = response.json()
        if not data or 'targets' not in data:
            return None
            
        # Step 3: Download from multiple targets and measure speed
        total_bytes = 0
        start_time = time.time()
        
        for target in data['targets'][:3]:  # Use first 3 targets
            url = target.get('url')
            if not url:
                continue
                
            try:
                # Download for 5 seconds from each target
                response = requests.get(url, proxies=proxies, headers=headers, 
                                      timeout=10, stream=True)
                
                chunk_start = time.time()
                for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                    if chunk:
                        total_bytes += len(chunk)
                    
                    # Stop after 5 seconds per target
                    if time.time() - chunk_start > 5:
                        break
                        
            except Exception:
                continue
        
        # Calculate speed
        elapsed_time = time.time() - start_time
        if elapsed_time > 0 and total_bytes > 0:
            # Convert to Mbps: (bytes * 8) / (seconds * 1,000,000)
            speed_mbps = (total_bytes * 8) / (elapsed_time * 1_000_000)
            return speed_mbps
            
        return None
        
    except Exception:
        return None


def _format_proxy_url(proxy: dict, scheme: str) -> str:
    """Format proxy URL with credentials."""
    return (
        f"{scheme}://{proxy['username']}:{proxy['password']}@"
        f"{proxy['host']}:{proxy['port']}"
    )

