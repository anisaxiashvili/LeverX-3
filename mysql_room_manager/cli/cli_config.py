"""CLI configuration settings."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CLIConfig:
    """CLI-specific configuration."""

    table_format: str = "grid"  
    max_display_rows: int = 50
    truncate_long_text: bool = True
    max_text_length: int = 50

    use_colors: bool = True
    header_color: str = "\033[1;34m" 
    success_color: str = "\033[1;32m" 
    warning_color: str = "\033[1;33m"  
    error_color: str = "\033[1;31m"   
    reset_color: str = "\033[0m"       
    show_timing: bool = True
    show_progress: bool = True

