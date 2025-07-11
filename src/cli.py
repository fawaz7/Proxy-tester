# src/cli.py

import argparse
import os
import re

def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Proxidize: Proxy Tester — A multi-threaded proxy testing tool"
    )

    parser.add_argument("proxy", nargs="?", help="Single proxy or path to proxy list file")
    parser.add_argument("--socks", action="store_true", help="Use SOCKS5 proxy")
    parser.add_argument("--http", action="store_true", help="Use HTTP proxy")
    parser.add_argument("--geo", action="store_true", help="Enable IP geolocation lookup")
    parser.add_argument("--speed-test", action="store_true", help="Include download speed test using speedtest-cli")
    parser.add_argument("-o", "--output", help="Output file path - specify format with extension (.txt default, .csv available)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug output")

    return parser.parse_args()

def interactive_prompt(args):
    config = {}    # Proxy source
    if args.proxy:
        config["proxy_input"] = args.proxy
    else:
        print("Enter proxies (one per line, then press Enter on an empty line to finish):")
        print("(You can paste multiple lines at once or enter them one by one)")
        lines = []
        proxy_count = 1
        
        while True:
            try:
                user_input = input(f"{proxy_count}. ").strip()
                if not user_input:
                    break
                
                # Check if user pasted multiple lines (common when copying from clipboard)
                # This handles cases where newlines are present in the input
                if '\n' in user_input or '\r' in user_input:
                    # Split on both types of newlines and filter empty lines
                    pasted_lines = re.split(r'[\r\n]+', user_input)
                    pasted_lines = [line.strip() for line in pasted_lines if line.strip()]
                    
                    for line in pasted_lines:
                        if line:
                            lines.append(line)
                            print(f"    Added proxy {proxy_count}: {line}")
                            proxy_count += 1
                else:
                    lines.append(user_input)
                    proxy_count += 1
                    
            except (EOFError, KeyboardInterrupt):
                print()  # New line for clean output
                break
        
        if lines:
            print(f"Total proxies entered: {len(lines)}")
        config["proxy_input"] = lines

    # Proxy type
    if args.socks:
        config["type"] = "socks"
    elif args.http:
        config["type"] = "http"
    else:
        choice = input("Choose proxy type [http/socks]: ").strip().lower()
        config["type"] = "socks" if "s" in choice else "http"

    # Geo-IP LookUp - only ask if not already specified
    if args.geo:
        config["geo_lookup"] = True
    else:
        # Only ask if --geo flag was not provided
        geo = input("Enable Geo-IP lookup? [y/N]: ").strip().lower()
        config["geo_lookup"] = geo == "y"

    # Speed test - only ask if not already specified  
    if args.speed_test:
        config["speed_test"] = True
    else:
        # Only ask if --speed-test flag was not provided
        speed = input("Include download speed test? [y/N]: ").strip().lower()
        config["speed_test"] = speed == "y"

    # Verbose mode
    config["verbose"] = args.verbose

    # Output file - don't ask here, we'll ask after results are shown
    if args.output:
        config["output_path"] = args.output
    else:
        config["output_path"] = None
        config["ask_for_output"] = True  # Flag to ask later

    return config
