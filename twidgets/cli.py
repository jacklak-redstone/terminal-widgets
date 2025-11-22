import argparse
import sys
import shutil
from pathlib import Path
from . import main as app_main

from importlib.resources import files, as_file


def init_command(args):
    """
    Handles the 'twidgets init' subcommand.
    """

    # 1. Define source and destination paths
    try:
        # 'twidgets.config' maps to the 'twidgets/config/' directory
        source_config_dir_traversable = files("twidgets.config")
    except ModuleNotFoundError:
        print("Error: Could not find the package config files. Is 'twidgets' installed correctly?", file=sys.stderr)
        sys.exit(1)

    dest_config_dir = Path.home() / ".config" / "twidgets"

    # 2. Create destination directory
    try:
        dest_config_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created config directory: {dest_config_dir}")
    except OSError as e:
        print(f"Error: Could not create directory {dest_config_dir}. {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Copy files
    # We must use 'as_file' to get a concrete Path on the filesystem
    with as_file(source_config_dir_traversable) as source_config_path:

        print(f"Copying YAML, ENV & TXT files from package config to {dest_config_dir}...")

        # Use rglob to find all YAML & ENV files recursively
        yaml_files = list(source_config_path.rglob("*.yaml"))
        yaml_files.extend(list(source_config_path.rglob("*.yml")))
        env_files = list(source_config_path.rglob("*.env"))
        txt_files = list(source_config_path.rglob("*.txt"))

        if not yaml_files and not env_files and not txt_files:
            print("Warning: No YAML, ENV & TEXT files found in the package config.", file=sys.stderr)
            return

        for source_file in yaml_files + env_files + txt_files:
            # Recreate the relative path in the destination
            relative_path = source_file.relative_to(source_config_path)
            dest_file = dest_config_dir / relative_path

            # Ensure the file's parent directory exists in the destination
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Requirement 2: Check for --force flag
            if not dest_file.exists() or args.force:
                try:
                    shutil.copy2(source_file, dest_file)
                    print(f"  Copied: {relative_path}")
                except OSError as e:
                    print(f"  Error copying {relative_path}: {e}", file=sys.stderr)
            else:
                print(f"  Skipped (exists): {relative_path}")

    print("\nInitialization complete.")
    print(f"Your configuration files are in: {dest_config_dir}")


def main():
    """
    Main entry point for the 'twidgets' command.
    """
    parser = argparse.ArgumentParser(description="Terminal Widgets main command.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ... (your 'init_parser' code stays the same) ...
    init_parser = subparsers.add_parser("init", help="Initialize user configuration files.")
    init_parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite existing configuration files."
    )
    init_parser.set_defaults(func=init_command)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        try:
            app_main.main_entry_point()
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)


if __name__ == "__main__":
    main()
