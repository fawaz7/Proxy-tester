from pyfiglet import Figlet
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table
from rich.text import Text
from colorama import Fore, Style
import src.config as config_module
from src import __version__

# Initialize colorama for Windows compatibility
init(autoreset=True)

console = Console()

def print_banner():
    figlet = Figlet(font='doom')
    title = figlet.renderText('Proxidize ')
    
    print(Fore.YELLOW + title)
    print(Fore.YELLOW + "----------------------------------------------------------")
    print(Fore.WHITE + "Proxy Tester: " + Fore.WHITE + "A multi-threaded proxy testing tool  " + Fore.GREEN + f"v{__version__}")
    print(Fore.YELLOW + "----------------------------------------------------------")
    print(Style.RESET_ALL)

def print_separator():
    print(Fore.YELLOW + "----------------------------------------------------------")

def print_info(message: str):
    print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + message)

def print_debug(message: str):
    """Print debug messages in gray, but only if verbose mode is enabled"""
    if config_module.VERBOSE_MODE:
        print(Fore.WHITE + "[DEBUG] " + Style.DIM + message + Style.RESET_ALL)

def print_success(message: str):
    print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + message)

def print_warning(message: str):
    print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + message)

def print_error(message: str):
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + message)

def print_result(result: dict, show_location: bool = False):
    """
    Nicely prints a single proxy test result with color.
    Only shows location if show_location is True.
    """
    status = result.get("Status", "Unknown")
    status_color = {
        "Working": Fore.GREEN,
        "Failed": Fore.RED,
        "Timeout": Fore.YELLOW
    }.get(status, Fore.WHITE)

    # Base output
    output = [
        f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} {status_color}[{status}]{Style.RESET_ALL} {result['IP']}"
    ]
    
    # Only add location if enabled and available
    if show_location and result.get('Location') not in ('N/A', None, ''):
        output.append(f"  Location: {Fore.GREEN}{result['Location']}{Style.RESET_ALL}")
    
    # Always show latency
    output.append(f"  Latency: {Fore.YELLOW}{result['Latency']}{Style.RESET_ALL}")
    
    print('\n'.join(output))

def display_result_table(results: list, show_location: bool = False, show_speed: bool = False):
    """
    Displays results in a rich table format with original ordering.
    Only includes columns based on user preferences.
    """
    if not results:
        print_warning("No results to display.")
        return

    # Sort results by original index to maintain input order
    results.sort(key=lambda x: x.get('original_index', 0))

    # Build table
    table = Table(title="Proxy Test Results")
    table.add_column("#", style="dim", no_wrap=True)  # Add numbering column
    table.add_column("Proxy Type", style="cyan", no_wrap=True)
    table.add_column("IP Address", style="yellow")
    
    if show_location:
        table.add_column("Location", style="green")
    
    table.add_column("Latency", style="magenta")
    
    if show_speed:
        table.add_column("Speed", style="green")
    
    table.add_column("Status", style="bold")

    for idx, result in enumerate(results, 1):  # Start numbering at 1
        status_text = Text(result.get("Status", "-"))

        if result.get("Status") == "Working":
            status_text.stylize("bold green")
        elif result.get("Status") == "Failed":
            status_text.stylize("bold red")
        else:
            status_text.stylize("yellow")

        row = [
            str(idx),  # Display number
            result.get("Type", "-"),
            result.get("IP", "-")
        ]

        if show_location:
            row.append(result.get("Location", "-"))

        row.append(result.get("Latency", "-"))

        if show_speed:
            row.append(result.get("Speed", "-"))

        row.append(status_text)

        table.add_row(*row)

    console.print(table)