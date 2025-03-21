"""
Shared templates used across pkgmngr modules.
"""
import os
import re
from pkgmngr.common.utils import sanitize_package_name

class DotNotationTemplate:
    """Template class that supports dot notation for accessing nested properties."""
    
    def __init__(self, template_content):
        """Initialize with template content."""
        self.template_content = template_content
    
    def render(self, config):
        """
        Render the template with the given configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            str: Rendered template
        """
        # Add computed properties
        enhanced_config = config.copy()
        
        # Replace all placeholders like ${name} or ${github.username}
        def replace_placeholder(match):
            key_path = match.group(1)
            return self._get_nested_value(enhanced_config, key_path)
        
        pattern = r'\${([a-zA-Z0-9_.]+)}'
        return re.sub(pattern, replace_placeholder, self.template_content)
    
    def _get_nested_value(self, config, key_path):
        """
        Get a value from a nested dictionary using dot notation.
        
        Args:
            config: Configuration dictionary
            key_path: Path to the value (e.g., 'github.username')
            
        Returns:
            The value at the specified path, or empty string if not found
        """
        parts = key_path.split('.')
        current = config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return ""  # Return empty string for missing values
        
        return str(current)


def _load_template(template_name):
    """
    Load template content from a file.
    
    Args:
        template_name: Name of the template file without extension
        
    Returns:
        str: Template content
    """
    try:
        # For Python 3.9+: Using importlib.resources.files
        from importlib.resources import files
        template_path = files('pkgmngr.templates').joinpath(f"{template_name}.txt")
        return template_path.read_text(encoding='utf-8')
    except (ImportError, AttributeError):
        # Fallback for older Python versions
        package_dir = os.path.dirname(os.path.dirname(__file__))
        template_path = os.path.join(package_dir, "templates", f"{template_name}.txt")
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
        
def render_template(template_name, base_dir=None, computed_properties=None):
    """
    Load configuration and render a template with dot notation support.
    
    Args:
        template_name: Name of the template to render
        base_dir: Optional base directory for loading config (default: current directory)
        
    Returns:
        str: Rendered template content
    """

    #default computed properties
    computed=dict(
        sanitized_name=lambda config: sanitize_package_name(config['package_name'])
    )

    if isinstance(computed_properties, dict):
        computed.update(computed_properties)

    # Load configuration
    from pkgmngr.common.config import load_config
    config, _ = load_config(base_dir)
    
    # Add computed properties
    for key in computed:
        config[key]=computed[key](config)


    # Load the template
    template_content = _load_template(template_name)
    
    # Render and return
    template = DotNotationTemplate(template_content)
    return template.render(config)