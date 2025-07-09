# src/cli.py

import argparse
import os

def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Proxidize: Proxy Tester — A multi-threaded proxy testing tool"
    )

    parser.add_argument("proxy", nargs="?", help="Single proxy or path to proxy list file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-T", "--timeout", type=int, default=30, help="Request timeout in seconds (default: 30)")
    parser.add_argument("--sock", action="store_true", help="Use SOCKS5 proxy")
    parser.add_argument("--http", action="store_true", help="Use HTTP proxy")
    parser.add_argument("--geo", action="store_true", help="Enable IP geolocation lookup")
    parser.add_argument("--speed-test", action="store_true", help="Include download speed test using speedtest-cli")
    parser.add_argument("-o", "--output", help="Output file path")

    return parser.parse_args()

def interactive_prompt(args):
    config = {}

    # Proxy source
    if args.proxy:
        config["proxy_input"] = args.proxy
    else:
        print("Enter proxies (one per line, then press Enter on an empty line to finish):")
        lines = []
        while True:
            line = input().strip()
            if not line:
                break
            lines.append(line)

        config["proxy_input"] = lines

    # Proxy type
    if args.sock:
        config["type"] = "socks"
    elif args.http:
        config["type"] = "http"
    else:
        choice = input("Choose proxy type [http/socks]: ").strip().lower()
        config["type"] = "socks" if "s" in choice else "http"

    # Gro-IP LookUp
    if args.geo:
        config["geo_lookup"] = True
    else:
        geo = input("Enable Geo-IP lookup? [y/N]: ").strip().lower()
        config["geo_lookup"] = geo == "y"

    # Speed test
    speed = input("Include download speed test? [y/N]: ").strip().lower()
    config["speed_test"] = speed == "y"

    # Threads
    config["threads"] = args.threads

    # Timeout
    config["timeout"] = args.timeout

    # Output file
    if args.output:
        config["output_path"] = args.output
    else:
        save = input("Save results to file? [y/N]: ").strip().lower()
        if save == "y":
            config["output_path"] = input("Enter output path (e.g., results.csv): ").strip()
        else:
            config["output_path"] = None

    return config
