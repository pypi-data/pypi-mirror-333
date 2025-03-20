"""
AigeoDB - Geographic database and utilities package.
"""

from .core.database import DatabaseManager
from .core.downloader import DatabaseDownloader

__version__ = "0.2.3"

__all__ = [
    "DatabaseManager",
    "DatabaseDownloader",
]
