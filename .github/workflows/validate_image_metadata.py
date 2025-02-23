import os
import subprocess
import sys
from pathlib import Path

from vision.utils.image import validate_image_metadata

if __name__ == "__main__":
    root = Path(
        os.environ.get(
            "GITHUB_WORKSPACE",
            subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
            .decode()
            .strip(),
        )
    )
    try:
        validate_image_metadata(root / "vision/vision/images")
    except ValueError as err:
        # Print the error string manually to prevent the stack trace from being logged.
        print(err, file=sys.stderr)
        sys.exit(1)
    print("✅ All image metadata is correct")
