# -*- coding: utf-8 -*-
"""
Printer utility for standardized console output formatting.

This module provides a centralized way to handle all console output
with consistent formatting, colors, and styling.
"""

from typing import Optional, List
from colorama import Fore, Style


class Printer:
    """
    Centralized printer for console output with consistent formatting.

    This class provides methods for different types of messages:
    - Info messages (light gray)
    - Success messages (green)
    - Warning messages (yellow)
    - Error messages (red)
    - Verbose messages (light black)
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the printer.

        Parameters
        ----------
        verbose : bool, optional
            Enable verbose output mode, default False
        """
        self.verbose = verbose

    def info(self, message: str, prefix: str = "~") -> None:
        """
        Print an info message.

        Parameters
        ----------
        message : str
            The message to print
        prefix : str, optional
            Prefix for the message, default "~"
        """
        print(f"{Fore.LIGHTBLACK_EX}{prefix} {message}{Style.RESET_ALL}")

    def success(self, message: str, prefix: str = "✓") -> None:
        """
        Print a success message.

        Parameters
        ----------
        message : str
            The message to print
        prefix : str, optional
            Prefix for the message, default "✓"
        """
        print(f"{Fore.GREEN}{prefix} {message}{Style.RESET_ALL}")

    def warning(self, message: str, prefix: str = "!") -> None:
        """
        Print a warning message.

        Parameters
        ----------
        message : str
            The message to print
        prefix : str, optional
            Prefix for the message, default "⚠️"
        """
        print(f"{Fore.YELLOW}{prefix} {message}{Style.RESET_ALL}")

    def error(self, message: str, prefix: str = "✗") -> None:
        """
        Print an error message.

        Parameters
        ----------
        message : str
            The message to print
        prefix : str, optional
            Prefix for the message, default "✗"
        """
        print(f"{Fore.RED}{prefix} {message}{Style.RESET_ALL}")

    def verbose_msg(self, message: str, prefix: str = "~") -> None:
        """
        Print a verbose message (only if verbose mode is enabled).

        Parameters
        ----------
        message : str
            The message to print
        prefix : str, optional
            Prefix for the message, default "~"
        """
        if self.verbose:
            print(f"{Fore.LIGHTBLACK_EX}{prefix} {message}{Style.RESET_ALL}")

    def action(self, message: str, prefix: str = "+") -> None:
        """
        Print an action message (blue color).

        Parameters
        ----------
        message : str
            The message to print
        prefix : str, optional
            Prefix for the message, default "+"
        """
        print(f"{Fore.BLUE}{prefix} {message}{Style.RESET_ALL}")

    def config_display(self, config_data: dict, title: str = "Configuration") -> None:
        """
        Display configuration data in a formatted ASCII art box.

        Parameters
        ----------
        config_data : dict
            Configuration data to display
        title : str, optional
            Title for the configuration display
        """
        # Print status message (always shown)
        self.action(f"[AppKernel] Loaded Application settings.")

        # Print configuration box (only in verbose mode)
        if self.verbose:
            print(f"{Fore.LIGHTBLACK_EX}...{Style.RESET_ALL}")
            print(
                f"{Fore.LIGHTBLACK_EX}   ┌───────────────────────────────────────────────┐{Style.RESET_ALL}"
            )
            for key, val in config_data.items():
                print(
                    f"{Fore.LIGHTBLACK_EX}   |- {key}: {Fore.LIGHTWHITE_EX}{val}{Style.RESET_ALL}"
                )
            print(
                f"{Fore.LIGHTBLACK_EX}   └───────────────────────────────────────────────┘{Style.RESET_ALL}"
            )
            print(f"{Fore.LIGHTBLACK_EX}...{Style.RESET_ALL}")

    def init(self, message: str, prefix: str = "🚀") -> None:
        """
        Print an initialization message (magenta/pink color).

        Parameters
        ----------
        message : str
            The message to print
        prefix : str, optional
            Prefix for the message, default "🚀"
        """
        print(f"{Fore.MAGENTA}{prefix} {message}{Style.RESET_ALL}")

    def section(self, title: str, prefix: str = "=") -> None:
        """
        Print a section header.

        Parameters
        ----------
        title : str
            The section title
        prefix : str, optional
            Character to use for the separator, default "="
        """
        separator = prefix * (len(title) + 4)
        print(f"{Fore.CYAN}{separator}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{prefix} {title} {prefix}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{separator}{Style.RESET_ALL}")

    def list_items(
        self, items: List[str], title: Optional[str] = None, max_items: int = 3
    ) -> None:
        """
        Print a list of items with optional title.

        Parameters
        ----------
        items : List[str]
            List of items to display
        title : str, optional
            Optional title for the list
        max_items : int, optional
            Maximum number of items to show before truncating, default 3
        """
        if title:
            self.info(title)

        if items:
            display_items = items[:max_items]
            items_str = ", ".join(display_items)
            if len(items) > max_items:
                items_str += "..."
            self.verbose_msg(f"   {items_str}")
        else:
            self.verbose_msg("   (no items)")

    def file_operation(
        self, operation: str, file_path: str, status: str = "completed"
    ) -> None:
        """
        Print a file operation message.

        Parameters
        ----------
        operation : str
            The operation performed (e.g., "Created", "Updated", "Deleted")
        file_path : str
            The file path
        status : str, optional
            Status of the operation, default "completed"
        """
        if status == "completed":
            self.info(f"[{operation}] {file_path}")
        elif status == "error":
            self.error(f"[{operation}] {file_path}")
        elif status == "warning":
            self.warning(f"[{operation}] {file_path}")

    def custom_print(
        self, message: str, color: str = "WHITE", prefix: str = ""
    ) -> None:
        """
        Print a custom message with specified color and prefix.

        Parameters
        ----------
        message : str
            The message to print
        color : str, optional
            Color name (WHITE, RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, LIGHTBLACK_EX, etc.)
            default "WHITE"
        prefix : str, optional
            Prefix for the message, default ""
        """
        color_attr = getattr(Fore, color.upper(), Fore.WHITE)
        prefix_part = f"{prefix} " if prefix else ""
        print(f"{color_attr}{prefix_part}{message}{Style.RESET_ALL}")

    def raw_print(self, message: str) -> None:
        """
        Print a raw message without any formatting or colors.

        Parameters
        ----------
        message : str
            The message to print directly
        """
        print(message)

    def qrc_compilation_result(
        self, success: bool, error_message: Optional[str] = None
    ) -> None:
        """
        Print QRC compilation result.

        Parameters
        ----------
        success : bool
            Whether compilation was successful
        error_message : str, optional
            Error message if compilation failed
        """
        if success:
            self.info("[FileMaker] Generated binaries definitions from QRC file.")
        else:
            self.warning("[FileMaker] QRC compilation skipped")
            if error_message:
                self.verbose_msg(f"Error details: {error_message}")


# Global printer instance for easy access
_default_printer = Printer()


def get_printer(verbose: bool = False) -> Printer:
    """
    Get a printer instance.

    Parameters
    ----------
    verbose : bool, optional
        Enable verbose mode, default False

    Returns
    -------
    Printer
        Printer instance
    """
    if verbose != _default_printer.verbose:
        return Printer(verbose)
    return _default_printer


def set_global_verbose(verbose: bool) -> None:
    """
    Set global verbose mode.

    Parameters
    ----------
    verbose : bool
        Enable or disable verbose mode
    """
    global _default_printer
    _default_printer = Printer(verbose)
