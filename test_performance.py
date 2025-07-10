#!/usr/bin/env python3
"""Performance and stress testing"""
import sys
import os
import time
sys.path.append('.')

from src.main import calculate_optimal_threads, initial_proxy_check
from src.utils import parse_proxy_line

print("=== PERFORMANCE & STRESS TESTING ===\n")

print("1. Testing thread calculation performance:")
start_time = time.time()
for i in range(1000):
    threads = calculate_optimal_threads(i)
end_time = time.time()
print(f"   ✅ 1000 thread calculations in {(end_time - start_time)*1000:.2f}ms")

print("\n2. Testing proxy parsing performance:")
test_proxy = "pg.proxi.es:20000:user:pass"
start_time = time.time()
for i in range(1000):
    parsed = parse_proxy_line(test_proxy)
end_time = time.time()
print(f"   ✅ 1000 proxy parsings in {(end_time - start_time)*1000:.2f}ms")

print("\n3. Testing large proxy list handling:")
large_proxy_list = []
for i in range(50):  # Create 50 test proxies
    large_proxy_list.append({
        'host': f'test{i}.example.com',
        'port': '8080',
        'username': f'user{i}',
        'password': f'pass{i}',
        'raw': f'test{i}.example.com:8080:user{i}:pass{i}',
        'type': 'http'
    })

optimal_threads = calculate_optimal_threads(len(large_proxy_list))
print(f"   ✅ {len(large_proxy_list)} proxies → {optimal_threads} threads")

print("\n4. Testing memory usage patterns:")
import gc
gc.collect()  # Clean up before test

# Simulate creating many proxy objects
proxy_objects = []
for i in range(1000):
    proxy_objects.append({
        'host': f'host{i}.com',
        'port': str(8000 + i),
        'username': f'user{i}',
        'password': f'pass{i}',
        'raw': f'host{i}.com:{8000+i}:user{i}:pass{i}',
        'type': 'http' if i % 2 == 0 else 'socks5'
    })

print(f"   ✅ Created {len(proxy_objects)} proxy objects successfully")

# Clean up
del proxy_objects
gc.collect()

print("\n✅ All performance tests completed successfully!")
