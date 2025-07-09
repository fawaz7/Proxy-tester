from pyfiglet import Figlet
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table
from rich.text import Text
from colorama import Fore, Style

# Initialize colorama for Windows compatibility
init(autoreset=True)

console = Console()

def print_banner():
    figlet = Figlet(font='doom')  # You can change font to 'standard', 'doom', etc.
    title = figlet.renderText('Proxidize ')
    
    print(Fore.YELLOW + title)
    print(Fore.YELLOW + "----------------------------------------------------------")
    print(Fore.WHITE + "Proxy Tester: " + Fore.WHITE + "A multi-threaded proxy testing tool  " + Fore.GREEN + "v1.00")
    print(Fore.YELLOW + "----------------------------------------------------------")
    print(Style.RESET_ALL)


def print_info(message: str):
    print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + message)

def print_success(message: str):
    print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + message)

def print_warning(message: str):
    print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + message)

def print_error(message: str):
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + message)


def print_result(result: dict):
    """
    Nicely prints a single proxy test result with color.
    """
    status = result.get("Status", "Unknown")
    status_color = {
        "Working": Fore.GREEN,
        "Failed": Fore.RED,
        "Timeout": Fore.YELLOW
    }.get(status, Fore.WHITE)

    print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} {status_color}[{status}]{Style.RESET_ALL} {result['IP']}")
    print(f"  Location: {Fore.GREEN}{result['Location']}{Style.RESET_ALL}")
    print(f"  Latency: {Fore.YELLOW}{result['Latency']}{Style.RESET_ALL}")


def display_result_table(results: list):
    if not results:
        print_warning("No results to display.")
        return

    # Determine if any result has speed/location
    include_speed = any("Speed" in r and r["Speed"] not in ("N/A", "", None) for r in results)
    include_location = any("Location" in r and r["Location"] not in ("N/A", "", None) for r in results)

    # Build table
    table = Table(title="Proxy Test Results")
    table.add_column("Proxy Type", style="cyan", no_wrap=True)
    table.add_column("IP Address", style="magenta")
    if include_location:
        table.add_column("Location", style="green")
    table.add_column("Latency", style="yellow")
    if include_speed:
        table.add_column("Speed", style="blue")
    table.add_column("Status", style="bold")

    for result in results:
        status_text = Text(result.get("Status", "-"))

        if result.get("Status") == "Working":
            status_text.stylize("bold green")
        elif result.get("Status") == "Failed":
            status_text.stylize("bold red")
        else:
            status_text.stylize("yellow")

        row = [
            result.get("Type", "-"),
            result.get("IP", "-")
        ]

        if include_location:
            row.append(result.get("Location", "-"))

        row.append(result.get("Latency", "-"))

        if include_speed:
            row.append(result.get("Speed", "-"))

        row.append(status_text)

        table.add_row(*row)

    console.print(table)



