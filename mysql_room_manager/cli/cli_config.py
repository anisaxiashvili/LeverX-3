"""CLI configuration settings."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CLIConfig:
    """CLI-specific configuration."""

    table_format: str = "grid"  # grid, simple, plain
    max_display_rows: int = 50
    truncate_long_text: bool = True
    max_text_length: int = 50

    use_colors: bool = True
    header_color: str = "\033[1;34m"  # Bold blue
    success_color: str = "\033[1;32m"  # Bold green
    warning_color: str = "\033[1;33m"  # Bold yellow
    error_color: str = "\033[1;31m"    # Bold red
    reset_color: str = "\033[0m"       # Reset

    show_timing: bool = True
    show_progress: bool = True

