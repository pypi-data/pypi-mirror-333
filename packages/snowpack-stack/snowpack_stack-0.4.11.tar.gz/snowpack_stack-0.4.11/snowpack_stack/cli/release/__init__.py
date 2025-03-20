"""Release CLI commands.

This package provides CLI commands for managing Snowpack Stack releases,
including checking versions, creating releases, and resetting versions.
"""

import sys
from pathlib import Path


def run_script(script_name: str, *args) -> int:
    """Run a script from the scripts directory.

    Args:
        script_name: Name of the script to run
        *args: Arguments to pass to the script

    Returns:
        int: Exit code from the script
    """
    # Import these functions only when needed to avoid circular imports
    from snowpack_stack.utils.subprocess_utils import run_command, validate_command_argument

    # Validate script name
    if not validate_command_argument(script_name):
        print(f"Error: Invalid script name: {script_name}")
        return 1

    # Validate all arguments
    for arg in args:
        if not validate_command_argument(str(arg)):
            print(f"Error: Invalid script argument: {arg}")
            return 1

    # Get the path to the scripts directory
    scripts_dir = Path(__file__).parent.parent.parent.parent / "scripts"
    script_path = scripts_dir / script_name

    if not script_path.exists():
        print(f"Error: Script {script_name} not found at {script_path}")
        return 1

    # Construct the command
    python_exe = sys.executable
    cmd = [python_exe, str(script_path)] + list(args)

    # Run the command
    try:
        result = run_command(cmd=cmd, check=True, capture_output=True, text=True)
        # Print output for visibility
        if result.stdout:
            print(result.stdout)
        return result.returncode
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return 1
