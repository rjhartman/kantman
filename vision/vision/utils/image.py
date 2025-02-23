"""Utils for loading and handling images."""

import re
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Tuple

import yaml
from pydantic import ValidationError
from pydantic.dataclasses import dataclass

METADATA_FILE_NAME = "metadata.yaml"
FILE_NAME_REGEX = r"^(?P<dice_set>\d+)_(?P<sides>\d+)_(?P<value>\d+)\.(jpg)|(png)$"


@dataclass(frozen=True)
class DiceImageMetadata:
    """Metadata of an image."""

    sides: int
    value: int


def _load_metadata_yaml(path: PathLike) -> Dict[str, Any]:
    if not Path(path).exists():
        raise FileNotFoundError("Expected metadata file to exist at {path}.")

    with open(path, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    if not isinstance(metadata, dict):
        raise ValueError(
            f"Invalid metadata at {path}: expected dict, got {type(metadata)}."
        )

    return metadata


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

    try:
        metadata = _load_metadata_yaml(metadata_path)
        return path, DiceImageMetadata(**metadata[path.name])
    except Exception as exc:
        if isinstance(exc, ValidationError):
            # The image was referenced in the metadata file, but schema was incorrect.
            # Reraise this exception.
            raise exc

    match = re.search(FILE_NAME_REGEX, path.name)
    if not match:
        raise ValueError(
            f'{path} was not found in a metadata yaml, and did not match file name regex "{FILE_NAME_REGEX}".'
        )

    sides = int(match.group("sides"))
    value = int(match.group("value"))

    return path, DiceImageMetadata(sides=sides, value=value)


def validate_image_metadata(directory: PathLike) -> None:
    """Validates that all metadata.yaml files in a directory are valid.

    Args:
        directory: The directory to validate.

    Raises:
        FileNotFoundError: The directory does not exist.
        ValueError: The provided path was not a directory, there were no metadata.yaml
                    files found, or one or more contained an error.
    """
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist.")

    if not path.is_dir():
        raise ValueError(f"{path} is not a directory.")

    def _format_error(file_path: Path, message: str) -> str:
        return f"{file_path.relative_to(path)}: {message}"

    errors = []
    metadata_file = None
    for metadata_file in Path(path).rglob("metadata.yaml"):
        parent_directory = metadata_file.parent
        try:
            metadata = _load_metadata_yaml(metadata_file)
        except (ValueError, FileNotFoundError) as err:
            errors.append(_format_error(metadata_file, str(err)))
            continue

        for filename, data in metadata.items():
            if not (parent_directory / filename).exists():
                errors.append(
                    _format_error(
                        metadata_file,
                        f"{filename} does not exist.",
                    )
                )
            try:
                DiceImageMetadata(**data)
            except ValidationError as err:
                errors.append(
                    _format_error(
                        metadata_file,
                        f"{filename} contains schema errors: {err.json()}",
                    )
                )

    if metadata_file is None:
        raise ValueError(f"No metadata.yaml files found in {path}.")

    if errors:
        error_string = (
            f"Encountered {len(errors)} error{'' if len(errors) == 1 else 's'}: \n\t"
        )
        error_string += "\n\t".join(errors)
        raise ValueError(error_string)


def process_new(set: int, dice: int, start_value) -> None:
    """Processes new images.

    Args:
        set:            The integer id for the dice set
        dice:           The number of sides on the dice (100 is just a d10 that increments the 10s place)
        start_value:    The starting value for the dice, most start at 1, but some start at 0
    """
    path_to_new = Path("vision/vision/new_images")
    multiplyer = 10 if dice == 100 else 1
    image_files = list(path_to_new.iterdir())
    image_files.sort()

    for i, image in enumerate(image_files):
        if image.is_file():
            new_file_name = ("_").join(
                [str(set), str(dice), str((start_value + i) * multiplyer)]
            ) + image.suffix
            image.rename(Path("vision/vision/images") / new_file_name)
            print(f"Renamed {image} to {new_file_name}")
