"""Utility helpers to work with speedtest-cli under authenticated proxies."""
from __future__ import annotations

import urllib.request
from typing import Dict
from urllib.parse import urlparse, urlunparse

from speedtest import Speedtest, SpeedtestResults


class BrowserLikeHTTPHandler(urllib.request.HTTPHandler):
    """HTTP handler that adds browser-like headers to all requests."""
    
    def http_open(self, req):
        # Add browser-like headers if not already present
        if not req.has_header('User-Agent'):
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        if not req.has_header('Accept'):
            req.add_header('Accept', '*/*')
        if not req.has_header('Accept-Language'):
            req.add_header('Accept-Language', 'en-US,en;q=0.9')
        return urllib.request.HTTPHandler.http_open(self, req)


class BrowserLikeHTTPSHandler(urllib.request.HTTPSHandler):
    """HTTPS handler that adds browser-like headers to all requests."""
    
    def https_open(self, req):
        # Add browser-like headers if not already present
        if not req.has_header('User-Agent'):
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        if not req.has_header('Accept'):
            req.add_header('Accept', '*/*')
        if not req.has_header('Accept-Language'):
            req.add_header('Accept-Language', 'en-US,en;q=0.9')
        return urllib.request.HTTPSHandler.https_open(self, req)


def build_requests_proxy(proxy: dict) -> Dict[str, str]:
    """Return a requests-compatible proxy mapping for the given proxy dict."""
    scheme = "socks5h" if proxy.get("type") == "socks5" else "http"
    proxy_url = _format_proxy_url(proxy, scheme)
    return {"http": proxy_url, "https": proxy_url}


def build_urllib_proxy_url(proxy: dict) -> str:
    """Return a urllib-compatible proxy URL for the given proxy dict."""
    scheme = "socks5" if proxy.get("type") == "socks5" else "http"
    return _format_proxy_url(proxy, scheme)


def redact_proxy_credentials(proxy_url: str) -> str:
    """Mask username/password from a proxy URL for safe logging."""
    if not proxy_url:
        return proxy_url

    parsed = urlparse(proxy_url)
    if parsed.username or parsed.password:
        netloc = parsed.hostname or ""
        if parsed.port:
            netloc = f"{netloc}:{parsed.port}"
        return urlunparse(
            (
                parsed.scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment,
            )
        )
    return proxy_url


def create_speedtest_with_proxy(proxy: dict, timeout: int = 25, secure: bool = False) -> Speedtest:
    """Instantiate a Speedtest client pre-configured to use the supplied proxy."""
    proxy_url = build_urllib_proxy_url(proxy)
    handler = urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})
    
    # Build opener with browser-like headers to avoid 403 errors
    opener = urllib.request.build_opener(
        handler,
        BrowserLikeHTTPHandler(),
        BrowserLikeHTTPSHandler(),
        urllib.request.HTTPDefaultErrorHandler(),
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPErrorProcessor()
    )
    
    # Set browser-like User-Agent
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
        ('Accept', '*/*'),
        ('Accept-Language', 'en-US,en;q=0.9')
    ]

    # Try with secure=False first for better compatibility
    st = Speedtest(timeout=timeout, secure=secure)
    st._opener = opener
    st._secure = secure
    
    if getattr(st, "results", None):
        st.results._opener = opener

    # Force configuration to be fetched through the proxy so the location is accurate.
    st.config = {}
    try:
        st.get_config()
    except Exception as e:
        # If secure fails, try without secure
        if secure:
            st._secure = False
            st.get_config()
        else:
            raise
    
    st.results = SpeedtestResults(
        client=st.config.get("client", {}),
        opener=opener,
        secure=st._secure,
    )

    # Clear cached server selections so subsequent lookups use the proxy's geo.
    st.servers = {}
    st.closest = []
    st._best = {}
    return st


def _format_proxy_url(proxy: dict, scheme: str) -> str:
    return (
        f"{scheme}://{proxy['username']}:{proxy['password']}@"
        f"{proxy['host']}:{proxy['port']}"
    )
