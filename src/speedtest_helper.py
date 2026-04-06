"""Utility helpers for Fast.com speed testing through proxies."""
from __future__ import annotations

import re
import time
import requests
from typing import Dict, Optional


def build_requests_proxy(proxy: dict) -> Dict[str, str]:
    """Return a requests-compatible proxy mapping for the given proxy dict."""
    scheme = "socks5h" if proxy.get("type") == "socks5" else "http"
    proxy_url = _format_proxy_url(proxy, scheme)
    return {"http": proxy_url, "https": proxy_url}


def _get_fast_com_token(proxies: dict, headers: dict, timeout: int) -> Optional[str]:
    """
    Fetch the Fast.com token by scraping the homepage to find the current
    JS bundle URL, then extracting the token from it.

    Fast.com uses a cache-busted JS filename (e.g. app-ed402d.js) that changes
    on every deploy, so hardcoding the URL breaks whenever they redeploy.
    """
    try:
        # Step 1: Fetch the homepage to find the current JS bundle URL
        home = requests.get(
            "https://fast.com/",
            proxies=proxies,
            headers=headers,
            timeout=timeout,
        )
        if home.status_code != 200:
            return None

        # Find the app JS bundle path: src="/app-XXXXXXXX.js"
        match = re.search(r'src="(/app-[a-f0-9]+\.js)"', home.text)
        if not match:
            return None

        js_url = "https://fast.com" + match.group(1)

        # Step 2: Fetch the JS bundle and extract the token
        js_resp = requests.get(js_url, proxies=proxies, headers=headers, timeout=timeout)
        if js_resp.status_code != 200:
            return None

        token_match = re.search(r'token:"([^"]+)"', js_resp.text)
        if not token_match:
            return None

        return token_match.group(1)

    except Exception:
        return None


def test_fast_com_speed(proxy: dict, timeout: int = 30) -> Optional[float]:
    """
    Test download speed using Fast.com API.
    Returns speed in Mbps or None if test fails.

    Fast.com uses Netflix's CDN servers for accurate speed testing.
    """
    try:
        proxies = build_requests_proxy(proxy)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Step 1: Get Fast.com token (scrapes homepage to find current JS bundle)
        token = _get_fast_com_token(proxies, headers, timeout)
        if not token:
            return None

        # Step 2: Get target URLs from Fast.com API
        api_url = f"https://api.fast.com/netflix/speedtest/v2?https=true&token={token}&urlCount=5"
        api_resp = requests.get(api_url, proxies=proxies, headers=headers, timeout=timeout)
        if api_resp.status_code != 200:
            return None

        data = api_resp.json()
        if not data or 'targets' not in data:
            return None

        # Step 3: Download from multiple targets and measure speed per target.
        # Measuring per-target avoids counting connection/handshake overhead in
        # the elapsed time, which inflates apparent latency and deflates speed.
        target_speeds = []

        for target in data['targets'][:3]:
            url = target.get('url')
            if not url:
                continue

            response = None
            try:
                response = requests.get(
                    url, proxies=proxies, headers=headers,
                    timeout=10, stream=True,
                )
                response.raise_for_status()

                downloaded = 0
                dl_start = time.time()

                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        downloaded += len(chunk)
                    if time.time() - dl_start > 5:
                        break

                dl_duration = time.time() - dl_start
                if downloaded > 0 and dl_duration > 0:
                    target_speeds.append((downloaded * 8) / (dl_duration * 1_000_000))

            except Exception:
                continue
            finally:
                if response is not None:
                    response.close()

        if not target_speeds:
            return None

        # Return the average speed across successful targets
        return sum(target_speeds) / len(target_speeds)

    except Exception:
        return None


def _format_proxy_url(proxy: dict, scheme: str) -> str:
    """Format proxy URL, with or without credentials."""
    if proxy.get('username') and proxy.get('password'):
        return (
            f"{scheme}://{proxy['username']}:{proxy['password']}@"
            f"{proxy['host']}:{proxy['port']}"
        )
    return f"{scheme}://{proxy['host']}:{proxy['port']}"
