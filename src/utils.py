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


def parse_proxy_line(line: str, proxy_type: str = None) -> dict:
    """
    Parses proxies in two formats:
    1. host:port:username:password
    2. username:password@host:port
    
    Supports both IPv4 addresses and DNS-based hostnames.
    
    Args:
        line: Raw proxy string
        proxy_type: 'http' or 'socks' (from --http/--socks flag or interactive prompt)
    
    Returns:
    {
        'host': 'pg.proxi.es' or '192.168.1.1',
        'port': '20000',
        'username': 'user',
        'password': 'pass',
        'raw': 'original_line',
        'type': 'http' or 'socks5'
    }
    
    Raises:
        ValueError: If proxy format is invalid or validation fails
    """
    import re
    
    line = line.strip()
    if not line:
        raise ValueError("Empty proxy line")
    
    host = None
    port = None
    username = None
    password = None
    
    # Format 1: username:password@host:port
    if '@' in line:
        # Split by @ to separate credentials from host:port
        parts = line.split('@')
        if len(parts) != 2:
            raise ValueError(f"Invalid proxy format (expected username:password@host:port): {line}")
        
        credentials, host_port = parts
        
        # Parse credentials
        cred_parts = credentials.split(':')
        if len(cred_parts) != 2:
            raise ValueError(f"Invalid credentials format (expected username:password): {credentials}")
        username, password = cred_parts
        
        # Parse host:port
        host_parts = host_port.split(':')
        if len(host_parts) != 2:
            raise ValueError(f"Invalid host:port format: {host_port}")
        host, port = host_parts
    
    # Format 2: host:port:username:password
    else:
        parts = line.split(':')
        if len(parts) != 4:
            raise ValueError(f"Invalid proxy format (expected host:port:username:password or username:password@host:port): {line}")
        
        host, port, username, password = parts
    
    # Validation
    if not host:
        raise ValueError("Host cannot be empty")
    
    if not port:
        raise ValueError("Port cannot be empty")
    
    # Validate port is numeric and in valid range
    try:
        port_num = int(port)
        if port_num < 1 or port_num > 65535:
            raise ValueError(f"Port must be between 1-65535, got: {port}")
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Port must be numeric, got: {port}")
        raise
    
    if not username:
        raise ValueError("Username cannot be empty")
    
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Validate IPv4 format if it looks like an IP
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', host):
        octets = host.split('.')
        for octet in octets:
            octet_num = int(octet)
            if octet_num < 0 or octet_num > 255:
                raise ValueError(f"Invalid IPv4 address: {host}")
    
    # Validate hostname format (basic DNS validation)
    elif not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-\.]*[a-zA-Z0-9])?$', host):
        raise ValueError(f"Invalid hostname format: {host}")
    
    # Build proxy dict
    proxy = {
        'host': host,
        'port': port,
        'username': username,
        'password': password,
        'raw': line,
    }
    
    # Type must come from user flag or interactive prompt, NOT from port inference
    if proxy_type:
        # Normalize type names
        if proxy_type.lower() in ['socks', 'socks5']:
            proxy['type'] = 'socks5'
        elif proxy_type.lower() == 'http':
            proxy['type'] = 'http'
        else:
            raise ValueError(f"Invalid proxy type: {proxy_type}. Must be 'http' or 'socks'")
    else:
        # If no type specified, this will be set later by the user config
        # Default to None and let the caller handle it
        proxy['type'] = None
    
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


