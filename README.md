# PNG to WebP Converter

A high-performance Python script to batch convert PNG images to WebP format with multithreading, GPU acceleration, and customizable quality settings.

## ✨ Features

- 🚀 **Multithreaded processing** - Dramatically faster batch conversions
- 🎯 **GPU acceleration** - NVIDIA CUDA support via FFmpeg
- 🔄 **Dual processing engines** - Choose between Pillow (CPU) or FFmpeg
- 📁 **Smart folder organization** - Automatically creates organized output folders
- 🎛️ **Flexible quality control** - Lossy, lossless, and custom quality options
- 🛡️ **Robust error handling** - Thread-safe processing with detailed progress reporting
- 🔍 **Case-insensitive detection** - Finds all PNG files regardless of case
- 🌟 **Transparency preservation** - Maintains PNG alpha channels

## 📋 Requirements

### Core Dependencies
- **Python 3.6+**
- **Pillow library**: `pip install Pillow`

### Optional (for GPU acceleration)
- **FFmpeg** with CUDA support
- **NVIDIA GPU** with compatible drivers
- **CUDA toolkit**

## 🚀 Quick Start

### Install Dependencies
```bash
pip install Pillow
```

### Basic Usage
```bash
# Convert all PNGs in a folder (single-threaded)
python png_to_webp.py /path/to/images

# Fast multithreaded conversion
python png_to_webp.py /path/to/images -t 4

# GPU-accelerated conversion
python png_to_webp.py /path/to/images --ffmpeg --gpu
```

## 📖 Detailed Usage

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `input_folder` | - | Path to folder containing PNG files | Required |
| `--output` | `-o` | Custom output folder path | `input_folder/webp_output` |
| `--quality` | `-q` | WebP quality (0-100) | 95 |
| `--lossless` | `-l` | Use lossless compression | False |
| `--threads` | `-t` | Number of processing threads | 1 |
| `--ffmpeg` | - | Use FFmpeg instead of Pillow | False |
| `--gpu` | - | Enable GPU acceleration | False |

### Processing Modes

#### 🔧 **Pillow Mode (Default)**
- **Best for**: Small to medium batches, simple setup
- **Pros**: Easy installation, reliable, good quality
- **Cons**: Slower for large batches

```bash
# Single-threaded
python png_to_webp.py ./images

# Multi-threaded (recommended)
python png_to_webp.py ./images -t 6
```

#### ⚡ **FFmpeg Mode**
- **Best for**: Large batches, advanced users
- **Pros**: Faster processing, GPU support
- **Cons**: Requires FFmpeg installation

```bash
# FFmpeg with 8 threads
python png_to_webp.py ./images --ffmpeg -t 8

# FFmpeg with GPU acceleration
python png_to_webp.py ./images --ffmpeg --gpu -t 2
```

## 🎯 Performance Guide

### Thread Recommendations

| System Type | Recommended Threads | Example Usage |
|-------------|-------------------|---------------|
| **4-core CPU** | 4-6 threads | `-t 4` |
| **8-core CPU** | 6-12 threads | `-t 8` |
| **16-core CPU** | 12-20 threads | `-t 16` |
| **GPU processing** | 1-2 threads | `--gpu -t 2` |

### Performance Comparison

| Method | Speed | Setup Difficulty | Best For |
|--------|--------|------------------|----------|
| Pillow (1 thread) | 1x | Easy | Testing, small batches |
| Pillow (8 threads) | 6x | Easy | Medium batches |
| FFmpeg (8 threads) | 8x | Medium | Large batches |
| FFmpeg + GPU | 15x | Hard | Massive batches |

## 💡 Usage Examples

### Basic Conversions
```bash
# Convert with default settings
python png_to_webp.py ./photos

# High quality conversion
python png_to_webp.py ./photos -q 98

# Lossless conversion
python png_to_webp.py ./artwork --lossless
```

### Performance Optimized
```bash
# Fast multi-threaded conversion
python png_to_webp.py ./batch_images -t 8 -q 85

# Maximum speed with GPU
python png_to_webp.py ./huge_dataset --ffmpeg --gpu -t 2

# Custom output location
python png_to_webp.py ./input -o ./compressed -t 6
```

### Specific Use Cases
```bash
# Web optimization (smaller files)
python png_to_webp.py ./website_images -q 80 -t 4

# Archive quality (perfect preservation)
python png_to_webp.py ./archives --lossless -t 2

# Production pipeline (balanced)
python png_to_webp.py ./production --ffmpeg -q 90 -t 8
```

## 📁 File Organization

The script automatically creates organized output:

```
your_images/
├── photo1.png
├── photo2.png
├── screenshot.PNG
└── webp_output/           # ← Auto-created
    ├── photo1.webp
    ├── photo2.webp
    └── screenshot.webp
```

## ⚙️ Quality Guidelines

| Quality Range | Use Case | File Size | Visual Quality |
|---------------|----------|-----------|---------------|
| **60-75** | Web thumbnails | Very small | Good |
| **75-85** | General web use | Small | Very good |
| **85-95** | High-quality images | Medium | Excellent |
| **95-100** | Professional work | Large | Near perfect |
| **Lossless** | Archival/editing | Largest | Perfect |

## 🔧 GPU Setup (Optional)

### NVIDIA GPU Requirements
1. **Compatible GPU**: GTX 900 series or newer
2. **NVIDIA drivers**: Latest version
3. **CUDA toolkit**: Version 11.0+
4. **FFmpeg with CUDA**: Compiled with `--enable-cuda`

### Verify GPU Support
```bash
# Check if FFmpeg supports CUDA
ffmpeg -hwaccels

# Test GPU conversion
python png_to_webp.py ./test_folder --ffmpeg --gpu -t 1
```

## 📊 Sample Output

```
Found 156 PNG files to convert using FFmpeg...
Using 8 thread(s) for processing
GPU acceleration enabled (requires compatible hardware)

✓ Converted (GPU): image001.png -> image001.webp
✓ Converted (GPU): photo_large.PNG -> photo_large.webp
✓ Converted (GPU): screenshot.png -> screenshot.webp
✗ Error converting corrupted.png: Invalid image format
✓ Converted (GPU): artwork.png -> artwork.webp

FFmpeg conversion complete! 155/156 files converted successfully.
```

## 🐛 Troubleshooting

### Common Issues

**"No PNG files found"**
```bash
# Check file extensions and path
ls *.png *.PNG
```

**GPU acceleration not working**
```bash
# Verify CUDA support
nvidia-smi
ffmpeg -hwaccels
```

**Out of memory with many threads**
```bash
# Reduce thread count for large images
python png_to_webp.py ./4k_images -t 2
```

**Permission errors**
```bash
# Check folder permissions
chmod 755 /path/to/folder
```

### Performance Tips

- **Large images**: Use fewer threads to avoid memory issues
- **Many small images**: Use more threads for better throughput
- **GPU mode**: Stick to 1-2 threads (GPU handles parallelism)
- **Mixed sizes**: Start with 4-6 threads and adjust

## 🔄 Migration from Other Tools

### From ImageMagick
```bash
# Old: magick *.png -quality 90 output_%03d.webp
# New: 
python png_to_webp.py ./ -q 90 -t 4
```

### From cwebp
```bash
# Old: for f in *.png; do cwebp "$f" -o "${f%.png}.webp"; done
# New:
python png_to_webp.py ./ -t 8
```

## 📈 Batch Processing Tips

### For Massive Datasets (1000+ images)
```bash
# Process in chunks to monitor progress
python png_to_webp.py ./chunk1 --ffmpeg --gpu -t 2
python png_to_webp.py ./chunk2 --ffmpeg --gpu -t 2
```

### For Production Workflows
```bash
# Create a processing script
#!/bin/bash
python png_to_webp.py ./raw_images --ffmpeg -q 90 -t 8 -o ./web_ready
python png_to_webp.py ./high_res --lossless -t 4 -o ./archive
```

## 🤝 Getting Help

```bash
# View all options
python png_to_webp.py --help

# Test with single file
python png_to_webp.py ./single_image_folder -t 1
```

## 📝 License

This script is provided as-is for educational and practical use. Feel free to modify and distribute.

---

**💡 Pro Tip**: Start with default settings and 4 threads, then optimize based on your hardware and needs!
