# reader.py
import os
from typing import Any, Dict
from .metadata import get_metadata

class ARWReader:
    """A class to read metadata from Sony .ARW raw image files."""
    def __init__(self, file_path: str) -> None:
        """Initialize with the path to an .ARW file."""
        if os.path.isabs(file_path):
            self.file_path = file_path
        else:
            self.file_path = os.path.abspath(file_path)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def get_metadata(self) -> Dict[str, Any]:
        """Extract all metadata from the .ARW file."""
        return get_metadata(self.file_path)

    def get_tag(self, tag: str) -> Any:
        """Get a specific metadata tag from the .ARW file."""
        meta = self.get_metadata()
        return meta.get(tag)