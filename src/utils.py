import os
import csv
import requests
from src.ui import print_info, print_warning, print_error


def load_proxies_from_file(filepath: str) -> list:
    """
    Reads a file line by line and returns a list of proxies.
    Ignores empty lines and comments (#).
    """
    proxies = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxies.append(line)
        print_info(f"Loaded {len(proxies)} proxies from {filepath}")
    except FileNotFoundError:
        print_error(f"Proxy file not found: {filepath}")
    return proxies


def format_latency(seconds: float) -> str:
    """
    Converts float seconds into human-readable latency string.
    Example: 0.256 -> '256ms'
    """
    return f"{int(seconds * 1000)}ms"


def parse_proxy_line(line: str) -> dict:
    """
    Parses proxies in format: host:port:username:password
    Supports both IP and DNS-based hostnames.
    Infers type based on port number (20002 for SOCKS5, 20000 for HTTP).

    Returns:
    {
        'host': 'pg.proxi.es',
        'port': 20000,
        'username': 'user',
        'password': 'pass',
        'raw': 'original_line',
        'type': 'http' or 'socks5'
    }
    """
    parts = line.strip().split(":")
    
    if len(parts) != 4:
        raise ValueError(f"Invalid proxy format: {line}")
        
    proxy = {
        'host': parts[0],
        'port': parts[1],
        'username': parts[2],
        'password': parts[3],
        'raw': line,
    }
    
    # Infer type based on port number
    if parts[1] == "20002":
        proxy['type'] = 'socks5'
    else:
        proxy['type'] = 'http'
    
    return proxy


def get_location_from_ip(ip: str) -> str:
    """
    Tries to resolve the location (City, Region, Country) for a given IP using:
    1. ip-api.com (free, no token, 45 req/min)
    2. ipwho.is as fallback
    """
    if not ip:
        return "N/A"

    try:
        # Try ip-api.com first
        ip_api_url = f"http://ip-api.com/json/{ip}"
        resp = requests.get(ip_api_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                city = data.get("city", "")
                region = data.get("regionName", "")
                country = data.get("country", "")
                return ", ".join(filter(None, [city, region, country]))
            elif data.get("status") == "fail":
                print_warning(f"[GEO] ip-api.com failed: {data.get('message', 'Unknown error')}")

    except Exception as e:
        print_warning(f"[GEO] ip-api.com exception → {e}")

    # Fallback: ipwho.is
    try:
        ipwho_url = f"https://ipwho.is/{ip}"
        resp = requests.get(ipwho_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success", False):
                city = data.get("city", "")
                region = data.get("region", "")
                country = data.get("country", "")
                return ", ".join(filter(None, [city, region, country]))
            else:
                print_warning(f"[GEO] ipwho.is failed: {data.get('message', 'Unknown error')}")

    except Exception as e:
        print_warning(f"[GEO] ipwho.is exception → {e}")

    return "N/A"


def save_results_to_file(results: list, filepath: str):
    """
    Saves proxy test results to a file based on the extension.
    Supports .csv and .txt formats.
    Saves directly to the specified path without creating data folders.
    Defaults to .txt format if no extension is specified.
    """
    # Determine format based on file extension
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext == '.csv':
        save_results_as_csv(results, filepath)
    elif file_ext == '.txt':
        save_results_as_txt(results, filepath)
    else:
        # Default to TXT if no extension or unknown extension
        if not file_ext:
            filepath += '.txt'
        save_results_as_txt(results, filepath)


def save_results_as_csv(results: list, filepath: str):
    """
    Saves proxy test results to a CSV file at the specified path.
    """
    fieldnames = ["Index", "Type", "IP", "Location", "Latency", "Speed", "Status"]
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for idx, row in enumerate(results, 1):
                filtered_row = {k: row.get(k, "") for k in fieldnames}
                filtered_row["Index"] = row.get("original_index", idx)
                # Ensure index is 1-based
                if isinstance(filtered_row["Index"], int):
                    filtered_row["Index"] = filtered_row["Index"] + 1 if filtered_row["Index"] == 0 else filtered_row["Index"]
                writer.writerow(filtered_row)
        print_info(f"Results saved to {filepath}")
    except Exception as e:
        print_error(f"Failed to save results: {str(e)}")


def save_results_as_txt(results: list, filepath: str):
    """
    Saves proxy test results to a TXT file at the specified path.
    """
    try:
        with open(filepath, mode='w', encoding='utf-8') as file:
            # Write header
            file.write("Index\tType\tIP\tLocation\tLatency\tSpeed\tStatus\n")
            for idx, row in enumerate(results, 1):
                index = row.get("original_index", idx)
                # Ensure index is 1-based
                if isinstance(index, int):
                    index = index + 1 if index == 0 else index
                file.write(f"{index}\t{row.get('Type','')}\t{row.get('IP','')}\t{row.get('Location','')}\t{row.get('Latency','')}\t{row.get('Speed','')}\t{row.get('Status','')}\n")
        print_info(f"Results saved to {filepath}")
    except Exception as e:
        print_error(f"Failed to save results: {str(e)}")


