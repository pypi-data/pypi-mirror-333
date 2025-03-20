"""
Error handling utilities for pkgmngr.
"""
import sys
import traceback
from typing import Optional, Callable, TypeVar, Any

# Type variable for the decorated function
F = TypeVar('F', bound=Callable[..., Any])


class PkgUtilsError(Exception):
    """Base exception class for pkgmngr errors."""
    pass


class ConfigError(PkgUtilsError):
    """Configuration-related errors."""
    pass


class GitError(PkgUtilsError):
    """Git-related errors."""
    pass


class GithubError(PkgUtilsError):
    """GitHub API-related errors."""
    pass


class SnapshotError(PkgUtilsError):
    """Snapshot-related errors."""
    pass


class RestoreError(PkgUtilsError):
    """Restore-related errors."""
    pass


class PackageError(PkgUtilsError):
    """Package creation or management errors."""
    pass


def handle_error(error: Exception, exit_code: int = 1, show_traceback: bool = False) -> None:
    """
    Handle an error consistently.
    
    Args:
        error: The exception that occurred
        exit_code: Exit code to use when exiting
        show_traceback: Whether to show the full traceback
    """
    if isinstance(error, PkgUtilsError):
        print(f"Error: {error}")
    else:
        print(f"Unexpected error: {error}")
    
    if show_traceback:
        traceback.print_exc()
    
    sys.exit(exit_code)


def error_handler(func: F) -> F:
    """
    Decorator for handling errors in CLI commands.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PkgUtilsError as e:
            handle_error(e)
        except Exception as e:
            handle_error(e, show_traceback=True)
    
    return wrapper  # type: ignore


def assert_condition(condition: bool, message: str, error_class: type = PkgUtilsError) -> None:
    """
    Assert that a condition is true, raising an error if it's not.
    
    Args:
        condition: The condition to check
        message: Error message if condition is False
        error_class: Exception class to raise (default: PkgUtilsError)
        
    Raises:
        The specified error class with the given message if condition is False
    """
    if not condition:
        raise error_class(message)


def try_operation(operation: Callable, error_message: str, 
                  error_class: type = PkgUtilsError, 
                  cleanup: Optional[Callable] = None) -> Any:
    """
    Try an operation, handling any exceptions with a custom error message.
    
    Args:
        operation: Function to try
        error_message: Error message if operation fails
        error_class: Exception class to raise (default: PkgUtilsError)
        cleanup: Optional cleanup function to call if operation fails
        
    Returns:
        Result of the operation
        
    Raises:
        The specified error class with the given message if operation fails
    """
    try:
        return operation()
    except Exception as e:
        if cleanup:
            try:
                cleanup()
            except Exception:
                # Ignore errors in cleanup
                pass
                
        # Add original error details to the message
        full_message = f"{error_message}: {str(e)}"
        raise error_class(full_message) from e