"""Utils for loading and handling images."""

from os import PathLike
from pathlib import Path
from typing import Tuple

import yaml
from pydantic.dataclasses import dataclass

METADATA_FILE_NAME = "metadata.yaml"


@dataclass(frozen=True)
class DiceImageMetadata:
    """Metadata of an image."""

    sides: int
    value: int


def load_image(_path: PathLike) -> Tuple[Path, DiceImageMetadata]:
    """Validates a path to an image and loads its metadata.

    Args:
        _path: Path to the image.

    Raises:
        ValueError: Path is a directory, the metadata file did not exist, or it was invalid.
        FileNotFoundError: File does not exist.

    Returns:
        A 2-tuple containing the path to the image and its metadata.
    """
    path = Path(_path)
    if path.is_dir():
        raise ValueError(f"{path} is a directory.")
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist.")

    metadata_path = path.parent / METADATA_FILE_NAME
    if not metadata_path.exists():
        raise ValueError("Expected metadata file to exist at {metadata_path}.")

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    if not isinstance(metadata, dict):
        raise ValueError(
            f"Invalid metadata at {metadata_path}: expected dict, got {type(metadata)}."
        )

    if path.name not in metadata:
        raise ValueError(
            "Expected to find metadata for {path.name} in {metadata_path}."
        )

    return path, DiceImageMetadata(**metadata[path.name])
