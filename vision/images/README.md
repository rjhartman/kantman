# Images

Contains images used for testing the vision software.

## Image Metadata

Each image should contain metadata for it located in a colocated `metadata.yaml` file. For the schema, see `vision.utils.image.DiceImageMetadata`. Example:
```yaml
# metadata.yaml
d6.png:
  sides: 6
  value: 5
```
