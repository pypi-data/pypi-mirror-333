# metadata.py
import exiftool
from typing import Dict, Any

def get_metadata(file_path: str) -> Dict[str, Any]:
    """Extract metadata from an .ARW file using ExifTool.

    This function uses pyexiftool to call ExifTool and retrieve all available
    metadata tags (e.g., EXIF, XMP, IPTC) from the specified .ARW file.

    Args:
        file_path (str): Path to the .ARW file (absolute or relative).

    Returns:
        Dict[str, Any]: A dictionary of metadata tags and their values.

    Raises:
        exiftool.exceptions.ExifToolExecuteError: If ExifTool fails to execute
            (e.g., not found in PATH or file processing error).
        IndexError: If no metadata is returned, indicating an invalid or
            unreadable file.
    """
    try:
        # Use ExifToolHelper, relying on exiftool being in the system PATH
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(file_path)[0]
        return metadata
    except exiftool.exceptions.ExifToolExecuteError as e:
        # Provide detailed error output for debugging
        raise exiftool.exceptions.ExifToolExecuteError(
            f"Failed to execute ExifTool: {e}\n"
            f"Standard Output: {e.stdout}\n"
            f"Standard Error: {e.stderr}"
        )
    except IndexError:
        raise IndexError("No metadata extracted. Ensure the file is a valid .ARW file.")