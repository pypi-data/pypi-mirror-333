"""Jimaku downloader package."""

from .downloader import JimakuDownloader

# Import and apply Windows socket compatibility early
try:
    from jimaku_dl.compat import windows_socket_compat

    windows_socket_compat()
except ImportError:
    # For backwards compatibility in case compat is not yet available
    pass

__version__ = "0.1.3"

__all__ = ["JimakuDownloader"]
