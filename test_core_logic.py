#!/usr/bin/env python3
"""Test script to verify thread calculation and other logic without signal handling"""
import sys
import os
sys.path.append('.')

print("Testing core logic functions...")

print("1. Testing thread calculation:")
from src.main import calculate_optimal_threads

test_cases = [
    (0, "zero proxies"),
    (1, "single proxy"),
    (10, "ten proxies"),
    (100, "hundred proxies"),
    (1000, "thousand proxies")
]

for proxy_count, description in test_cases:
    threads = calculate_optimal_threads(proxy_count)
    expected_range = (1, 64)  # Should be between 1 and 64
    if expected_range[0] <= threads <= expected_range[1]:
        print(f"   ✅ {description}: {proxy_count} → {threads} threads")
    else:
        print(f"   ❌ {description}: {proxy_count} → {threads} threads (out of range)")

print("\n2. Testing utility functions:")
from src.utils import format_latency

latency_tests = [
    (0.001, "1ms"),
    (0.1, "100ms"), 
    (1.0, "1000ms"),
    (2.5, "2500ms")
]

for seconds, expected in latency_tests:
    result = format_latency(seconds)
    if result == expected:
        print(f"   ✅ {seconds}s → {result}")
    else:
        print(f"   ❌ {seconds}s → {result} (expected {expected})")

print("\n3. Testing configuration loading:")
try:
    import src.config as config_module
    print(f"   ✅ Loaded config - Timeout: {config_module.REQUEST_TIMEOUT}s")
    print(f"   ✅ Speed test duration: {config_module.SPEED_TEST_DURATION}s")
    print(f"   ✅ API URL: {config_module.IP_API_URL}")
    print(f"   ✅ App name: {config_module.APP_NAME}")
    print(f"   ✅ App version: {config_module.APP_VERSION}")
except Exception as e:
    print(f"   ❌ Config loading failed: {e}")

print("\n✅ Core logic tests completed!")
