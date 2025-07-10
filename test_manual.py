#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

from src.utils import parse_proxy_line

print("Testing proxy parsing:")

# Test valid proxy
try:
    result = parse_proxy_line('host:8080:user:pass')
    print('✅ Valid proxy parsed:', result['host'])
except Exception as e:
    print('❌ Valid proxy failed:', e)

# Test invalid proxy (too few parts)
try:
    result = parse_proxy_line('invalid:proxy')
    print('❌ Invalid proxy unexpectedly succeeded:', result)
except ValueError as e:
    print('✅ Invalid proxy correctly rejected:', str(e))

print("\nTesting edge cases:")

# Empty string
try:
    result = parse_proxy_line('')
    print('❌ Empty string unexpectedly succeeded')
except ValueError as e:
    print('✅ Empty string correctly rejected:', str(e))

# Too many parts
try:
    result = parse_proxy_line('host:8080:user:pass:extra:parts')
    print('❌ Too many parts unexpectedly succeeded')
except ValueError as e:
    print('✅ Too many parts correctly rejected:', str(e))
