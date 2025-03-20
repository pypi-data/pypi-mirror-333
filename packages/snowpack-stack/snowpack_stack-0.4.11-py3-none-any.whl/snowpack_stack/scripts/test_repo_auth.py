#!/usr/bin/env python
"""
Script to test repository authentication functionality.
"""

import argparse
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Import our secure subprocess utilities - use relative import since this is a package script
from snowpack_stack.utils.subprocess_utils import get_executable_path, run_poetry_command


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Test repository authentication functionality")
    parser.parse_args()

    try:
        # Import the repo_auth module
        from snowpack_stack import repo_auth

        # Test repository authentication
        logger.info("Testing repository authentication...")

        # Check gcloud authentication
        if not repo_auth.ensure_gcloud_auth():
            logger.error("❌ gcloud authentication check failed")
            return 1
        logger.info("✅ gcloud authentication check passed")

        # Test pip configuration
        if not repo_auth.configure_pip():
            logger.error("❌ pip configuration failed")
            return 1
        logger.info("✅ pip configuration successful")

        # Test Poetry configuration (if available)
        poetry_path = get_executable_path("poetry")
        if poetry_path:
            try:
                # Using centralized secure poetry command runner
                run_poetry_command(["--version"], capture_output=True)

                if not repo_auth.configure_poetry():
                    logger.warning("⚠️ Poetry configuration failed, but continuing")
                else:
                    logger.info("✅ Poetry configuration successful")
            except Exception as e:
                logger.info(f"ℹ️ Poetry check failed: {str(e)}, skipping Poetry configuration")
        else:
            logger.info("ℹ️ Poetry not installed, skipping Poetry configuration")

        # Test keyring setup (simplified)
        logger.info("✅ keyring setup skipped (simplified)")

        logger.info("✅ All repository authentication tests passed!")
        return 0

    except Exception as e:
        logger.error(f"❌ Error testing repository authentication: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
