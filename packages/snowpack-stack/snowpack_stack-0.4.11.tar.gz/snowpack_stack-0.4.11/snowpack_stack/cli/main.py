"""Main CLI entry point for Snowpack Stack.

This module provides the main CLI entry point for Snowpack Stack,
with subcommands for building assets, setting up the environment,
and managing releases.
"""

import argparse
import sys
from typing import List, Optional

# Import the access control module
from snowpack_stack.access_control import (
    COMMANDS,
    AccessDeniedError,
    AccessLevel,
    KeyMissingError,
    check_command_access,
)


def run_build_command(args: argparse.Namespace) -> int:
    """Run the build command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    if hasattr(args, "bruin") and args.bruin:
        if hasattr(args, "asset_type") and args.asset_type:
            if args.asset_type == "yaml":
                from snowpack_stack.cli.build.bruin.yaml import main as yaml_main

                return yaml_main()
            elif args.asset_type == "sql":
                from snowpack_stack.cli.build.bruin.sql import main as sql_main

                return sql_main()
        else:
            from snowpack_stack.cli.build.bruin import main as bruin_main

            return bruin_main()
    else:
        from snowpack_stack.cli.build.all import main as all_main

        return all_main()


def run_setup_command(args: argparse.Namespace) -> int:
    """Run the setup command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Check for the new verify-internal command
    if hasattr(args, "setup_command") and args.setup_command == "verify-internal":
        from snowpack_stack.cli.setup.verify_internal import main as verify_internal_main

        return verify_internal_main()
    # Check for the rotate-key command
    elif hasattr(args, "setup_command") and args.setup_command == "rotate-key":
        try:
            # Check if the user has access to the rotate-key command
            check_command_access("setup", "rotate-key")

            from snowpack_stack.cli.setup.rotate_key import main as rotate_key_main

            return rotate_key_main()
        except AccessDeniedError as e:
            print(f"Error: {e}")
            return 1
        except KeyMissingError as e:
            print(f"Error: {e}")
            return 1
    elif hasattr(args, "setup_type") and args.setup_type:
        if args.setup_type == "auth":
            from snowpack_stack.cli.setup.auth import main as auth_main

            return auth_main(args)
        elif args.setup_type == "verify":
            from snowpack_stack.cli.setup.verify import main as verify_main

            return verify_main()
    else:
        # Run both auth and verify
        from snowpack_stack.cli.setup.auth import main as auth_main
        from snowpack_stack.cli.setup.verify import main as verify_main

        auth_result = auth_main(args)
        if auth_result != 0:
            return auth_result

        return verify_main()


def run_release_command(args: argparse.Namespace) -> int:
    """Run the release command.

    Args:
        args: Command line arguments

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Check access using the new access control system
        check_command_access("release")

        if hasattr(args, "release_command") and args.release_command:
            if args.release_command == "create":
                from snowpack_stack.cli.release.create import main as create_main

                return create_main(args)
            elif args.release_command == "check":
                from snowpack_stack.cli.release.check import main as check_main

                return check_main()
            elif args.release_command == "reset":
                from snowpack_stack.cli.release.reset import main as reset_main

                return reset_main(args)
            elif args.release_command == "changelog":
                from snowpack_stack.cli.release.changelog import main as changelog_main

                return changelog_main(args)
        else:
            # Show help for release command
            parser = create_release_parser()
            parser.print_help()
            return 0

    except AccessDeniedError as e:
        print(f"Error: {e}")
        print("\nThe following commands are available to you:")
        for cmd, details in COMMANDS.items():
            if details["access_level"] == AccessLevel.PUBLIC:
                print(f"  - {cmd}: {details['description']}")
        return 1

    except KeyMissingError as e:
        print(f"Error: {e}")
        return 1


def create_build_parser(subparsers):
    """Create the parser for the build command.

    Args:
        subparsers: Subparsers object from the main parser

    Returns:
        argparse.ArgumentParser: The build command parser
    """
    build_parser = subparsers.add_parser("build", help="Build assets")
    build_subparsers = build_parser.add_subparsers(dest="build_command")

    # All subcommand (default)
    all_parser = build_subparsers.add_parser("all", help="Build all assets")

    # Bruin subcommand
    bruin_parser = build_subparsers.add_parser("bruin", help="Build Bruin assets")
    bruin_parser.set_defaults(bruin=True)

    bruin_subparsers = bruin_parser.add_subparsers(dest="asset_type")
    yaml_parser = bruin_subparsers.add_parser("yaml", help="Build Bruin YAML assets")
    sql_parser = bruin_subparsers.add_parser("sql", help="Build Bruin SQL assets")

    return build_parser


def create_setup_parser(subparsers):
    """Create the parser for the setup command.

    Args:
        subparsers: Subparsers object from the main parser

    Returns:
        argparse.ArgumentParser: The setup command parser
    """
    setup_parser = subparsers.add_parser("setup", help="Setup commands")
    setup_subparsers = setup_parser.add_subparsers(dest="setup_type")

    # Auth subcommand
    auth_parser = setup_subparsers.add_parser("auth", help="Authentication setup")
    auth_parser.add_argument("--email", help="Email address for authentication")

    # Verify subcommand
    verify_parser = setup_subparsers.add_parser("verify", help="Verify installation")

    # Add verify-internal command
    verify_internal_parser = setup_subparsers.add_parser(
        "verify-internal", help="Verify internal developer access"
    )

    # Add rotate-key command
    rotate_key_parser = setup_subparsers.add_parser(
        "rotate-key", help="Generate a new API key (internal access only)"
    )

    # Store the subcommand name
    verify_internal_parser.set_defaults(setup_command="verify-internal")
    rotate_key_parser.set_defaults(setup_command="rotate-key")

    return setup_parser


def create_release_parser(subparsers=None):
    """Create the parser for the release command.

    Args:
        subparsers: Subparsers object from the main parser

    Returns:
        argparse.ArgumentParser: The release command parser
    """
    if subparsers:
        release_parser = subparsers.add_parser(
            "release", help="Release management commands (internal access only)"
        )
    else:
        release_parser = argparse.ArgumentParser(
            prog="snowpack release",
            description="Release management commands (internal access only)",
        )

    release_subparsers = release_parser.add_subparsers(dest="release_command")

    # Create subcommand
    create_parser = release_subparsers.add_parser("create", help="Create a new release")
    create_parser.add_argument(
        "version_bump",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Version component to bump",
    )
    create_parser.add_argument(
        "--set", dest="specific_version", help="Set a specific version instead of bumping"
    )
    create_parser.add_argument(
        "--no-push", action="store_true", help="Don't push changes to remote"
    )

    # Check subcommand
    check_parser = release_subparsers.add_parser("check", help="Check if a version exists")

    # Reset subcommand
    reset_parser = release_subparsers.add_parser("reset", help="Reset a version")
    reset_parser.add_argument("version", help="Version to reset (e.g., '0.4.1')")

    # Changelog subcommand
    changelog_parser = release_subparsers.add_parser("changelog", help="Generate a changelog")
    changelog_parser.add_argument(
        "--from", dest="from_ref", help="Starting reference (tag or commit)"
    )
    changelog_parser.add_argument(
        "--to", dest="to_ref", default="HEAD", help="Ending reference (tag or commit)"
    )
    changelog_parser.add_argument("--output", help="Output file (default: stdout)")

    return release_parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(description="Snowpack Stack CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Create subcommand parsers
    create_build_parser(subparsers)
    create_setup_parser(subparsers)
    create_release_parser(subparsers)

    # Parse arguments
    args = parser.parse_args(args)

    # Run the appropriate command
    if args.command == "build":
        return run_build_command(args)
    elif args.command == "setup":
        return run_setup_command(args)
    elif args.command == "release":
        return run_release_command(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
