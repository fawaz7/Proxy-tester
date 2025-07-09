import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.cli import parse_cli_args, interactive_prompt
from src.utils import load_proxies_from_file, parse_proxy_line
from src.proxy_tester import test_http_proxy, test_socks_proxy
from src.ui import print_banner, print_info, print_result, display_result_table, print_error
from src.utils import save_results_to_csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def main():
    print_banner()

    args = parse_cli_args()
    config = interactive_prompt(args)

    if isinstance(config["proxy_input"], list):
        raw_proxies = config["proxy_input"]
    elif config["proxy_input"].endswith(".txt"):
        raw_proxies = load_proxies_from_file(config["proxy_input"])
    else:
        raw_proxies = [config["proxy_input"]]


    proxies = []
    for p in raw_proxies:
        proxy = parse_proxy_line(p)
        proxy["speed_test"] = config.get("speed_test", False)
        proxy["geo_lookup"] = config.get("geo_lookup", False)
        proxies.append(proxy)
    
    test_func = test_socks_proxy if config["type"] == "socks" else test_http_proxy

    results = []

    print_info(f"Testing {len(proxies)} proxies using {config['threads']} threads...")

    with ThreadPoolExecutor(max_workers=config["threads"]) as executor:
        future_to_proxy = {executor.submit(test_func, proxy): proxy for proxy in proxies}

        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                print_result(result)
                results.append(result)
            except Exception as e:
                print_error(f"[THREAD FAIL] {proxy['raw']} → {e}")

    display_result_table(results)

    if config["output_path"]:
        save_results_to_csv(results, config["output_path"])

if __name__ == "__main__":
    main()