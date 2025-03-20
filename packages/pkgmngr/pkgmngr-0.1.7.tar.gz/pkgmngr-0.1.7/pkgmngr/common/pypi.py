"""
Functions to check package name availability on PyPI.
"""
import requests
from pkgmngr.common.cli import display_warning, display_info, display_success
from pkgmngr.common.errors import try_operation

def is_name_available_on_pypi(package_name):
    """
    Check if a package name is available on PyPI.
    
    Args:
        package_name: Name to check
        
    Returns:
        bool: True if the name is available, False if it's taken
    """
    try:
        # Query the PyPI API for the package
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        
        # If status code is 404, the package doesn't exist (name is available)
        if response.status_code == 404:
            return True
        
        # If status code is 200, the package exists (name is taken)
        elif response.status_code == 200:
            return False
        
        # For other status codes, assume it might be available but warn about the error
        else:
            display_warning(f"Couldn't verify PyPI availability due to API error: {response.status_code}")
            return True
            
    except requests.RequestException as e:
        # If there's a connection error, assume it might be available but warn
        display_warning(f"Couldn't connect to PyPI to check name availability: {str(e)}")
        return True

def check_name_availability(package_name, context="create"):
    """
    Check package name availability and display appropriate messages.
    
    Args:
        package_name: Name to check
        context: Context of the check ('create' or 'rename')
        
    Returns:
        bool: True if the check passed (name is available or user confirmed)
    """
    is_available = is_name_available_on_pypi(package_name)
    
    if is_available:
        display_success(f"Package name '{package_name}' is available on PyPI.")
        return True
    else:
        action_text = "create" if context == "create" else "rename to"
        display_warning(f"Package name '{package_name}' is already taken on PyPI!")
        display_info(f"You can still {action_text} the package with this name for local development,")
        display_info(f"but you won't be able to publish it to PyPI without choosing a different name.")
        
        # Ask for confirmation to proceed
        user_input = input(f"Do you want to continue with '{package_name}' anyway? (y/n): ").lower()
        return user_input in ['y', 'yes']