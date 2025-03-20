"""
mcp-perforce - 用于与Perforce Swarm系统交互的工具
"""

from .perforce import (
    mcp,
    get_changelist_files_catalog,
    get_file_details,
    analysis_file,
)

from .main import main

__version__ = "0.1.4" 