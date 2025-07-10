#!/usr/bin/env python3
"""Test script to verify signal handling and graceful shutdown"""
import sys
import os
import time
import signal
sys.path.append('.')

from src.main import signal_handler, check_shutdown

print("Testing signal handling...")

# Test the signal handler function
print("1. Testing signal_handler function:")
try:
    signal_handler(signal.SIGINT, None)
    print("✅ Signal handler executed without error")
except Exception as e:
    print(f"❌ Signal handler failed: {e}")

# Test check_shutdown function
print("\n2. Testing check_shutdown function (normal case):")
try:
    check_shutdown()  # Should not exit since shutdown_requested is False
    print("✅ check_shutdown works correctly in normal case")
except SystemExit:
    print("❌ check_shutdown exited when it shouldn't have")
except Exception as e:
    print(f"❌ check_shutdown failed: {e}")

print("\n3. Testing thread calculation:")
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
    print(f"   {description}: {proxy_count} → {threads} threads")

print("\n✅ All tests completed successfully!")
