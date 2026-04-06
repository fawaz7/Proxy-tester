# test_ui.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui import print_banner, print_info, print_success, print_warning, print_error, display_result_table

sample_results = [
    {"Type": "HTTP", "IP": "23.45.67.89", "Location": "Dallas, TX", "Latency": "110ms", "Speed": "N/A", "Status": "Working"},
    {"Type": "SOCKS5", "IP": "98.76.54.32", "Location": "Seattle, WA", "Latency": "250ms", "Speed": "N/A", "Status": "Working"},
    {"Type": "HTTP", "IP": "N/A", "Location": "N/A", "Latency": "N/A", "Speed": "N/A", "Status": "Failed"},
]


def test_print_banner_does_not_raise():
    print_banner()


def test_print_info_does_not_raise():
    print_info("Test info message")


def test_print_success_does_not_raise():
    print_success("Test success message")


def test_print_warning_does_not_raise():
    print_warning("Test warning message")


def test_print_error_does_not_raise():
    print_error("Test error message")


def test_display_result_table_does_not_raise():
    display_result_table(sample_results)


def test_display_result_table_with_location():
    display_result_table(sample_results, show_location=True)


def test_display_result_table_with_speed():
    display_result_table(sample_results, show_speed=True)


def test_display_result_table_empty():
    display_result_table([])


if __name__ == "__main__":
    test_print_banner_does_not_raise()
    test_print_info_does_not_raise()
    test_print_success_does_not_raise()
    test_print_warning_does_not_raise()
    test_print_error_does_not_raise()
    test_display_result_table_does_not_raise()
    test_display_result_table_with_location()
    test_display_result_table_with_speed()
    test_display_result_table_empty()
    print("All UI tests passed.")
