"""
Common CLI utilities for pkgmngr.
"""
import os
import sys
from typing import Optional, List, Any, Dict, Tuple
from pathlib import Path


def confirm_action(prompt: str, default: bool = False) -> bool:
    """
    Ask for user confirmation.
    
    Args:
        prompt: The confirmation prompt to display
        default: Default value if user presses enter
        
    Returns:
        True if user confirmed, False otherwise
    """
    default_text = "Y/n" if default else "y/N"
    user_input = input(f"{prompt} [{default_text}]: ").strip().lower()
    
    if not user_input:
        return default
    
    return user_input in ('y', 'yes')


def get_input_with_default(prompt: str, default: Optional[str] = None) -> str:
    """
    Get user input with optional default value.
    
    Args:
        prompt: The prompt to display
        default: Default value to use if user presses enter
        
    Returns:
        User input or default value
    """
    default_text = f" [{default}]" if default is not None else ""
    user_input = input(f"{prompt}{default_text}: ").strip()
    
    if not user_input and default is not None:
        return default
    
    return user_input


def select_from_list(options: List[str], prompt: str = "Select an option:") -> Optional[int]:
    """
    Present a numbered list of options for the user to select from.
    
    Args:
        options: List of options to display
        prompt: The prompt to display
        
    Returns:
        Selected index or None if cancelled
    """
    if not options:
        print("No options available.")
        return None
    
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice = input("\nEnter number (or q to quit): ").strip()
            
            if choice.lower() in ('q', 'quit', 'exit'):
                return None
                
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Please enter a valid number.")


def get_git_commit_message() -> Optional[str]:
    """
    Prompt the user for a Git commit message.
    
    Returns:
        Commit message or None if cancelled
    """
    print("Enter a commit message (or 'q' to cancel):")
    message = input("> ").strip()
    
    if message.lower() in ('q', 'quit', 'exit'):
        return None
        
    if not message:
        return "Update package files"
        
    return message


def display_success(message: str) -> None:
    """
    Display a success message to the user.
    
    Args:
        message: The message to display
    """
    print(f"\n✅ {message}")


def display_warning(message: str) -> None:
    """
    Display a warning message to the user.
    
    Args:
        message: The message to display
    """
    print(f"\n⚠️  {message}")


def display_error(message: str) -> None:
    """
    Display an error message to the user.
    
    Args:
        message: The message to display
    """
    print(f"\n❌ {message}")


def display_info(message: str) -> None:
    """
    Display an information message to the user.
    
    Args:
        message: The message to display
    """
    print(f"\nℹ️  {message}")


def display_command_help(command: str, description: str, examples: List[str] = None) -> None:
    """
    Display help information for a command.
    
    Args:
        command: The command name
        description: Description of the command
        examples: Optional list of usage examples
    """
    print(f"\n{command}\n{'=' * len(command)}")
    print(f"\n{description}\n")
    
    if examples:
        print("Examples:")
        for example in examples:
            print(f"  {example}")
        print()


def print_table(headers: List[str], rows: List[List[Any]], min_widths: List[int] = None) -> None:
    """
    Print a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of rows, each row being a list of values
        min_widths: Optional minimum width for each column
    """
    if not rows:
        print("No data to display.")
        return
        
    # Determine column widths
    col_widths = [len(h) for h in headers]
    
    if min_widths:
        col_widths = [max(min_w, w) for min_w, w in zip(min_widths, col_widths)]
    
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    
    # Print header
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))
    
    # Print rows
    for row in rows:
        row_values = [str(val).ljust(col_widths[i]) for i, val in enumerate(row)]
        print(" | ".join(row_values))