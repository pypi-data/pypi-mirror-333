import argparse
import sys
from pathlib import Path
from .core import list_directory

def main():
    parser = argparse.ArgumentParser(
        description="Display directory structure in a tree-like format"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to list (default: current directory)",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        help="Maximum depth to traverse",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Show hidden files and directories",
    )
    parser.add_argument(
        "-f",
        "--files-only",
        action="store_true",
        help="Show only files (no directories)",
    )
    parser.add_argument(
        "-D",
        "--dirs-only",
        action="store_true",
        help="Show only directories (no files)",
    )
    parser.add_argument(
        "-e",
        "--exclude-empty",
        action="store_true",
        help="Exclude empty directories",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        help="Include only files matching this pattern (e.g., '*.pdf')",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        help="Exclude files matching this pattern",
    )
    parser.add_argument(
        "--min-size",
        type=int,
        help="Minimum file size in bytes",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        help="Maximum file size in bytes",
    )

    args = parser.parse_args()

    try:
        for line in list_directory(
            args.directory,
            max_depth=args.max_depth,
            show_hidden=args.all,
            only_files=args.files_only,
            only_dirs=args.dirs_only,
            exclude_empty=args.exclude_empty,
            file_pattern=args.pattern,
            exclude_pattern=args.exclude,
            min_size=args.min_size,
            max_size=args.max_size
        ):
            print(line)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 