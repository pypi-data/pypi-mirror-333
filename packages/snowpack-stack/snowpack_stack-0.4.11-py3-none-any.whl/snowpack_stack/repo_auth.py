"""
Repository authentication module for Snowpack Stack.

This module is now a compatibility layer since Snowpack Stack is available directly from PyPI.
Previous functionality for configuring pip and Poetry to use the custom repository is kept for backward compatibility.
"""

import logging
import sys
from pathlib import Path

# Import our secure subprocess utilities instead of using subprocess directly

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants - kept for backward compatibility
REPOSITORY_URL = "us-west1-python.pkg.dev/snowpack-dev/snowpack-stack"
REPOSITORY_ALIAS = "snowpack"
PIP_CONFIG_FILE = Path.home() / ".pip" / "pip.conf"
POETRY_CONFIG_FILE = Path.home() / ".config" / "pypoetry" / "config.toml"


def ensure_gcloud_auth() -> bool:
    """
    Simplified function that pretends to ensure the user is authenticated with gcloud.
    This is now a no-op that always returns True.

    Returns:
        bool: Always True
    """
    logger.info("Snowpack Stack is now available directly from PyPI - no gcloud auth needed")
    return True


def run_gcloud_auth_login() -> bool:
    """
    Simplified function that pretends to run gcloud auth login.
    This is now a no-op that always returns True.

    Returns:
        bool: Always True
    """
    logger.info("Snowpack Stack is now available directly from PyPI - no gcloud auth needed")
    return True


def configure_pip() -> bool:
    """
    No-op function that pretends to configure pip.
    Since the package is now available on PyPI, no special configuration is needed.

    Returns:
        bool: Always True
    """
    logger.info("Snowpack Stack is now available directly from PyPI - no pip configuration needed")
    return True


def configure_poetry() -> bool:
    """
    No-op function that pretends to configure Poetry.
    Since the package is now available on PyPI, no special configuration is needed.

    Returns:
        bool: Always True
    """
    logger.info(
        "Snowpack Stack is now available directly from PyPI - no Poetry configuration needed"
    )
    return True


def setup_repository_auth() -> bool:
    """
    No-op function for backward compatibility.
    Since the package is now available on PyPI, no repository auth is needed.

    Returns:
        bool: Always True
    """
    logger.info("Snowpack Stack is now available directly from PyPI - no repository auth needed")
    return True


def check_dependencies() -> bool:
    """
    No-op function for backward compatibility.
    Since the package is now available on PyPI, no special dependencies are needed.

    Returns:
        bool: Always True
    """
    logger.info(
        "Snowpack Stack is now available directly from PyPI - no special dependencies needed"
    )
    return True


def main() -> int:
    """
    Main entry point for repository authentication CLI.
    Now just returns success for backward compatibility.

    Returns:
        int: Always 0 (success)
    """
    logger.info("Snowpack Stack is now available directly from PyPI - no repository auth needed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
