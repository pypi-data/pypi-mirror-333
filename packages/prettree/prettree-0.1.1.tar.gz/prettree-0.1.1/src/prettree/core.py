import os
from pathlib import Path
from typing import Optional, Iterator

class TreeNode:
    def __init__(self, path: Path, is_last: bool = False, indent: str = ""):
        self.path = Path(path)
        self.is_last = is_last
        self.indent = indent

def list_directory(
    directory: str | Path = ".",
    max_depth: Optional[int] = None,
    show_hidden: bool = False,
    only_files: bool = False,
    only_dirs: bool = False,
    exclude_empty: bool = False,
    file_pattern: Optional[str] = None,
    exclude_pattern: Optional[str] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None
) -> Iterator[str]:
    """
    Generate a tree-like structure of directories and files.
    
    Args:
        directory: The starting directory path
        max_depth: Maximum depth to traverse (None for unlimited)
        show_hidden: Whether to show hidden files and directories
        only_files: Show only files (no directories)
        only_dirs: Show only directories (no files)
        exclude_empty: Skip empty directories
        file_pattern: Include only files matching this pattern (e.g., "*.pdf")
        exclude_pattern: Exclude files matching this pattern
        min_size: Minimum file size in bytes
        max_size: Maximum file size in bytes
    
    Yields:
        Formatted strings representing the tree structure
    """
    directory = Path(directory)
    
    def should_include(path: Path) -> bool:
        # Skip hidden files unless explicitly shown
        if not show_hidden and path.name.startswith('.'):
            return False
            
        # Apply file/directory filters
        if only_files and path.is_dir():
            return False
        if only_dirs and path.is_file():
            return False
            
        # Check if directory is empty
        if exclude_empty and path.is_dir():
            try:
                next(path.iterdir(), None)
            except (PermissionError, OSError):
                return False
            
        # Apply pattern filters
        if path.is_file():
            if file_pattern and not path.match(file_pattern):
                return False
            if exclude_pattern and path.match(exclude_pattern):
                return False
                
            # Apply size filters
            size = path.stat().st_size
            if min_size is not None and size < min_size:
                return False
            if max_size is not None and size > max_size:
                return False
                
        return True
    
    def walk_directory(node: TreeNode, depth: int = 0) -> Iterator[str]:
        if max_depth is not None and depth > max_depth:
            return

        if should_include(node.path):
            # Add size information for files
            if node.path.is_file():
                size = node.path.stat().st_size
                size_str = f" ({size:,} bytes)"
            else:
                size_str = ""
                
            yield f"{node.indent}{'└── ' if node.is_last else '├── '}{node.path.name}{size_str}"

            if node.path.is_dir():
                entries = [p for p in node.path.iterdir() if should_include(p)]
                entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
                
                for idx, entry in enumerate(entries):
                    is_last = idx == len(entries) - 1
                    new_indent = node.indent + ('    ' if node.is_last else '│   ')
                    yield from walk_directory(
                        TreeNode(entry, is_last, new_indent),
                        depth + 1
                    )

    yield directory.absolute().as_posix()
    entries = [p for p in directory.iterdir() if should_include(p)]
    entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    
    for idx, entry in enumerate(entries):
        is_last = idx == len(entries) - 1
        yield from walk_directory(TreeNode(entry, is_last)) 