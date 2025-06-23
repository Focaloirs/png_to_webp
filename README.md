# PNG to WebP Converter

A simple Python script to batch convert PNG images to WebP format with customizable quality settings.

## Features

- 🔄 Batch convert all PNG files in a folder
- 🎯 High-quality conversion with customizable quality settings
- 🔒 Lossless compression option for perfect quality preservation
- 📁 Flexible output folder options
- 🛡️ Error handling and progress reporting
- 🔍 Case-insensitive PNG file detection
- 🌟 Preserves transparency from PNG files

## Installation

### Prerequisites

- Python 3.6 or higher
- Pillow library

### Install Dependencies

```bash
pip install Pillow
```

## Usage

### Basic Usage

Convert all PNG files in a folder:
```bash
python png_to_webp.py /path/to/your/folder
```

### Advanced Usage

**Specify output folder:**
```bash
python png_to_webp.py /path/to/input -o /path/to/output
```

**Set custom quality (0-100):**
```bash
python png_to_webp.py /path/to/folder -q 85
```

**Use lossless compression:**
```bash
python png_to_webp.py /path/to/folder --lossless
```

**Combine options:**
```bash
python png_to_webp.py ./images -o ./webp_output -q 90
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `input_folder` | - | Path to folder containing PNG files | Required |
| `--output` | `-o` | Output folder path | Same as input folder |
| `--quality` | `-q` | WebP quality (0-100) | 95 |
| `--lossless` | `-l` | Use lossless compression | False |

## Examples

### Example 1: Basic Conversion
```bash
python png_to_webp.py ./images
```
Converts all PNG files in `./images` folder to WebP with 95% quality.

### Example 2: High Compression
```bash
python png_to_webp.py ./photos -q 80 -o ./compressed
```
Converts PNG files with 80% quality and saves to `./compressed` folder.

### Example 3: Perfect Quality
```bash
python png_to_webp.py ./artwork --lossless
```
Converts PNG files using lossless compression for perfect quality preservation.

## Output

The script provides real-time feedback:

```
Found 5 PNG files to convert...
✓ Converted (quality 95): image1.png -> image1.webp
✓ Converted (quality 95): photo.PNG -> photo.webp
✗ Error converting corrupted.png: cannot identify image file
✓ Converted (quality 95): screenshot.png -> screenshot.webp
✓ Converted (quality 95): logo.png -> logo.webp

Conversion complete! 4/5 files converted successfully.
```

## Quality Guidelines

| Quality Setting | Use Case | File Size | Quality |
|----------------|----------|-----------|---------|
| 85-95 | General web use | Small | Excellent |
| 95-100 | High-quality images | Medium | Near perfect |
| Lossless | Archival/editing | Large | Perfect |

## File Handling

- **Input**: Supports `.png` and `.PNG` files
- **Output**: Creates `.webp` files with the same base filename
- **Transparency**: Preserves alpha channel from PNG files
- **Errors**: Skips corrupted files and continues processing

## Benefits of WebP Format

- **Smaller file sizes**: 25-50% smaller than PNG
- **Better compression**: Superior to PNG while maintaining quality
- **Modern browser support**: Supported by all major browsers
- **Transparency support**: Maintains PNG transparency features

## Troubleshooting

### Common Issues

**"No PNG files found"**
- Check that your folder path is correct
- Ensure PNG files exist in the specified folder

**"Error: Input folder does not exist"**
- Verify the folder path exists
- Use absolute paths if relative paths aren't working

**"Permission denied"**
- Ensure you have write permissions for the output folder
- Try running with appropriate permissions

### Getting Help

```bash
python png_to_webp.py --help
```

## License

This script is provided as-is for educational and practical use. Feel free to modify and distribute.

## Contributing

Feel free to submit issues, feature requests, or improvements to enhance this tool.

---

**Note**: Always backup your original PNG files before conversion, especially when using the same folder for input and output.
