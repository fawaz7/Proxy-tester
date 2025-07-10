import sys
import os
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
import math
from typing import List, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cli import parse_cli_args, interactive_prompt
from src.utils import load_proxies_from_file, parse_proxy_line, save_results_to_csv
from src.proxy_tester import test_http_proxy, test_socks_proxy, run_speed_test, run_geo_lookup
from src.ui import print_banner, print_info, print_result, display_result_table, print_error, print_success, print_warning, print_debug, print_separator
import src.config as config_module

# Global flag for graceful shutdown
shutdown_requested = False

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully with a visually appealing message"""
    global shutdown_requested
    shutdown_requested = True
    
    print_separator()
    print_info("Proxidize received interrupt signal (Ctrl+C)")
    print_info("Allowing current operations to complete safely...")
    print_info("Press Ctrl+C again to force exit (not recommended)")
    print_separator()

def check_shutdown():
    """Check if shutdown was requested and exit gracefully if needed"""
    if shutdown_requested:
        print_success("Thank you for using our tool!")
        sys.exit(0)

def calculate_optimal_threads(proxy_count: int, base_threads: int = 8, max_threads: int = 64) -> int:
    """Calculate optimal thread count based on proxy count."""
    if proxy_count <= 0:
        return 1
    calculated = base_threads * math.log2(proxy_count + 1)
    rounded = round(calculated)
    return min(max(rounded, 1), min(max_threads, proxy_count))

def initial_proxy_check(proxies: List[Dict[str, Any]], user_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Perform initial fast connectivity check only"""
    test_func = test_socks_proxy if user_config["type"] == "socks" else test_http_proxy
    thread_count = calculate_optimal_threads(len(proxies))
    print_separator()
    print_info(f"Starting initial connectivity check for {len(proxies)} proxies...")
    print_debug(f"Thread calculation: {len(proxies)} proxies → {thread_count} threads")
    print_debug(f"Test function: {'SOCKS5' if user_config['type'] == 'socks' else 'HTTP'}")
    
    results = [None] * len(proxies)
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        future_to_index = {
            executor.submit(test_func, proxy): i 
            for i, proxy in enumerate(proxies)
        }
        
        for future in as_completed(future_to_index):
            # Check for shutdown request
            check_shutdown()
            
            idx = future_to_index[future]
            proxy = proxies[idx]
            try:
                result = future.result()
                # Pass show_location=False for initial check
                print_result(result, show_location=False)
                results[idx] = result
            except Exception as e:
                print_error(f"[THREAD FAIL] {proxy['raw']} → {str(e)}")
                results[idx] = {
                    "Type": user_config["type"].upper(),
                    "IP": "N/A",
                    "Location": "N/A",
                    "Latency": "N/A",
                    "Speed": "N/A",
                    "Status": "Failed",
                    "Error": str(e)
                }
    
    working_count = sum(1 for r in results if r and r["Status"] == "Working")
    print()
    print_success(f"Initial check complete! {working_count}/{len(proxies)} proxies working")
    print_separator()
    return results

def perform_additional_checks(working_proxies: List[Dict[str, Any]], user_config: Dict[str, Any]) -> None:
    """Perform optional additional checks (geo-IP and speed tests)"""
    if not working_proxies:
        return
    
    # Geo-IP lookups
    if user_config.get("geo_lookup"):
        geo_threads = calculate_optimal_threads(len(working_proxies), base_threads=8, max_threads=32)
        print_separator
        print_info(f"Starting Geo-IP lookups for {len(working_proxies)} proxies...")
        print_debug(f"Geo-IP threads: {len(working_proxies)} proxies → {geo_threads} threads")
        
        with ThreadPoolExecutor(max_workers=geo_threads) as executor:
            futures = [
                executor.submit(run_geo_lookup, proxy, result)
                for proxy, result in working_proxies
            ]
            for future in as_completed(futures):
                # Check for shutdown request
                check_shutdown()
                try:
                    future.result()
                except Exception as e:
                    print_error(f"[GEO LOOKUP ERROR] {str(e)}")
        print_success("Geo-IP lookups completed")
        print_separator()
    
    # Speed tests
    if user_config.get("speed_test"):
        speed_threads = calculate_optimal_threads(len(working_proxies), base_threads=4, max_threads=16)
        print_separator()
        print_info(f"Starting speed tests for {len(working_proxies)} proxies...")
        print_debug(f"Speed test threads: {len(working_proxies)} proxies → {speed_threads} threads")
        print_debug(f"Speed test config: Duration={config_module.SPEED_TEST_DURATION}s, Min data={config_module.MIN_TEST_BYTES/1024/1024:.1f}MB")
        
        with ThreadPoolExecutor(max_workers=speed_threads) as executor:
            futures = [
                executor.submit(run_speed_test, proxy, result)
                for proxy, result in working_proxies
            ]
            for future in as_completed(futures):
                # Check for shutdown request
                check_shutdown()
                try:
                    future.result()
                except Exception as e:
                    print_error(f"[SPEEDTEST ERROR] {str(e)}")
        print_success("Speed tests completed")
        print_separator()

def main():
    """Main function that orchestrates the proxy testing process"""
    # Register signal handler for graceful Ctrl+C handling
    # Handle both SIGINT (Ctrl+C) and SIGTERM for better cross-platform support
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    print_banner()
    
    # Parse command line arguments and get user configuration
    args = parse_cli_args()
    user_config = interactive_prompt(args)
    
    # Set verbose mode globally for debug output
    config_module.VERBOSE_MODE = user_config.get("verbose", False)
    
    if user_config.get("verbose"):
        print_info("Verbose mode enabled - showing detailed debug information")
        print_debug(f"Configuration: Type={user_config.get('type')}, Geo={user_config.get('geo_lookup')}, Speed={user_config.get('speed_test')}")
        print_debug(f"Output file: {user_config.get('output_path', 'None specified')}")
        print_debug(f"Signal handlers registered: SIGINT{' and SIGTERM' if hasattr(signal, 'SIGTERM') else ''}")
        print_debug(f"Graceful shutdown system: ✅ Active")

    # Validate and load proxies
    try:
        if isinstance(user_config["proxy_input"], list):
            raw_proxies = user_config["proxy_input"]
        elif user_config["proxy_input"].endswith(".txt"):
            if not os.path.exists(user_config["proxy_input"]):
                print_error(f"❌ Proxy file not found: {user_config['proxy_input']}")
                return
            raw_proxies = load_proxies_from_file(user_config["proxy_input"])
        else:
            raw_proxies = [user_config["proxy_input"]]
        
        if not raw_proxies:
            print_error("❌ No proxies found to test")
            return
            
    except Exception as e:
        print_error(f"❌ Error loading proxies: {str(e)}")
        return

    # Parse and validate proxy format
    proxies = []
    for i, proxy_line in enumerate(raw_proxies):
        try:
            parsed_proxy = parse_proxy_line(proxy_line)
            if parsed_proxy:
                proxies.append(parsed_proxy)
            else:
                print_warning(f"⚠️ Skipping invalid proxy format: {proxy_line}")
        except Exception as e:
            print_warning(f"⚠️ Error parsing proxy line {i+1}: {proxy_line} - {str(e)}")
    
    if not proxies:
        print_error("❌ No valid proxies found after parsing")
        return
    
    print_info(f"Successfully parsed {len(proxies)} valid proxies")
    
    # Check for shutdown before starting tests
    check_shutdown()
    
    # Phase 1: Initial connectivity check
    results = initial_proxy_check(proxies, user_config)
    
    # Filter working proxies for additional checks
    working_proxies = [
        (proxies[i], results[i])
        for i in range(len(results))
        if results[i] and results[i]["Status"] == "Working"
    ]
    
    if not working_proxies:
        print_warning("No working proxies found - skipping additional checks")
    else:
        # Check for shutdown before additional checks
        check_shutdown()
        
        # Apply the additional check flags only to working proxies
        for proxy, _ in working_proxies:
            proxy["speed_test"] = user_config.get("speed_test", False)
            proxy["geo_lookup"] = user_config.get("geo_lookup", False)
        
        # Phase 2: Optional additional checks
        if user_config.get("geo_lookup") or user_config.get("speed_test"):
            perform_additional_checks(working_proxies, user_config)
    
    # Display final results
    print_separator()
    print_info("Displaying final results...")
    valid_results = [r for r in results if r]
    if valid_results:
        display_result_table(
            valid_results,
            show_location=user_config.get("geo_lookup", False),
            show_speed=user_config.get("speed_test", False)
        )
    else:
        print_warning("No results to display")
    
    # Save results to file if requested
    if user_config.get("output_path") and valid_results:
        try:
            save_results_to_csv(valid_results, user_config["output_path"])
            print_success(f"Results saved to: {user_config['output_path']}")
        except Exception as e:
            print_error(f"Failed to save results: {str(e)}")
    elif user_config.get("output_path"):
        print_warning("No results to save to file")
    print_separator()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Final fallback for any unhandled Ctrl+C
        print_separator()
        print_info("Proxidize was forcefully terminated")
        print_success("Thanks for using Proxidize: Proxy Tester!")
        print_separator()
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error occurred: {str(e)}")
        print_info("Please report this issue if it persists :)")
        sys.exit(1)