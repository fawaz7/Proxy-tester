from pyfiglet import Figlet
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
)
from rich.panel import Panel
from rich.live import Live
from colorama import Fore, Style
import src.config as config_module
from src import __version__

# Initialize colorama for Windows compatibility
init(autoreset=True)

console = Console()

def print_banner():
    figlet = Figlet(font='doom')
    title = figlet.renderText('FAWAZ')
    
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

def create_progress_bar(description: str = "Processing", transient: bool = False):
    """
    Create a beautiful Rich progress bar with all the bells and whistles.
    
    Args:
        description: The task description
        transient: If True, progress bar disappears when complete
    
    Returns:
        Progress object
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        MofNCompleteColumn(),
        TextColumn("│"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("│"),
        TimeElapsedColumn(),
        TextColumn("│"),
        TimeRemainingColumn(),
        console=console,
        transient=transient,
        expand=False,
    )

def print_speed_test_header(total_proxies: int):
    """Display a beautiful header for speed test phase"""
    header_text = f"""
[bold cyan]Speed Test Phase[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[yellow]Testing {total_proxies} proxies sequentially[/yellow]
[dim]• Each proxy tested individually for 100% accuracy
• Full bandwidth allocated per test
• ETA calculated in real-time[/dim]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    panel = Panel(
        header_text,
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)

def print_speed_test_result(proxy_num: int, total: int, ip: str, speed: str, location: str = None):
    """
    Print a beautiful inline result for each completed speed test
    
    Args:
        proxy_num: Current proxy number
        total: Total proxies
        ip: IP address
        speed: Speed result (e.g., "7.02 Mbps")
        location: Optional location string
    """
    # Determine speed color based on value
    if speed == "Error":
        speed_style = "[red]Error[/red]"
    else:
        try:
            speed_val = float(speed.replace(" Mbps", ""))
            if speed_val >= 10:
                speed_style = f"[bold green]{speed}[/bold green]"
            elif speed_val >= 5:
                speed_style = f"[green]{speed}[/green]"
            elif speed_val >= 1:
                speed_style = f"[yellow]{speed}[/yellow]"
            else:
                speed_style = f"[red]{speed}[/red]"
        except:
            speed_style = f"[dim]{speed}[/dim]"
    
    # Build result line
    result_line = f"[dim]#{proxy_num:02d}/{total:02d}[/dim] │ [cyan]{ip:15}[/cyan] │ {speed_style}"
    
    if location and location != "N/A":
        result_line += f" │ [dim]{location}[/dim]"
    
    console.print(result_line)

def print_summary_stats(total: int, working: int, failed: int, avg_time: float, avg_speed: float = None):
    """
    Display beautiful summary statistics at the end
    
    Args:
        total: Total proxies tested
        working: Number of working proxies
        failed: Number of failed proxies
        avg_time: Average time per test
        avg_speed: Average speed in Mbps (optional)
    """
    success_rate = (working / total * 100) if total > 0 else 0
    
    # Build summary text
    summary_lines = [
        f"[bold]Test Summary[/bold]",
        "",
        f"Total Proxies:    [cyan]{total}[/cyan]",
        f"Working:          [green]{working}[/green] ({success_rate:.1f}%)",
        f"Failed:           [red]{failed}[/red]",
        f"Avg Time:         [yellow]{avg_time:.1f}s[/yellow] per proxy",
    ]
    
    if avg_speed is not None:
        if avg_speed >= 10:
            speed_color = "bold green"
        elif avg_speed >= 5:
            speed_color = "green"
        elif avg_speed >= 1:
            speed_color = "yellow"
        else:
            speed_color = "red"
        summary_lines.append(f"Avg Speed:        [{speed_color}]{avg_speed:.2f} Mbps[/{speed_color}]")
    
    summary_text = "\n".join(summary_lines)
    
    panel = Panel(
        summary_text,
        border_style="green" if success_rate >= 70 else "yellow",
        padding=(1, 2),
        title="[bold]Results[/bold]",
    )
    console.print()
    console.print(panel)