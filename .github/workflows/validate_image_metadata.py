import sys
from pathlib import Path

from vision.utils.image import validate_image_metadata

if __name__ == "__main__":
    file = Path(__file__)
    try:
        validate_image_metadata(file.parent / "../../vision/vision/images")
    except ValueError as err:
        # Print the error string manually to prevent the stack trace from being logged.
        print(err, file=sys.stderr)
        sys.exit(1)
    print("✅ All image metadata is correct")
