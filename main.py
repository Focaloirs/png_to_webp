import os
import sys
import subprocess
from pathlib import Path
from PIL import Image
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def convert_single_png_ffmpeg(png_file, output_path, quality, use_gpu):
    """Convert a single PNG file to WebP using FFmpeg."""
    try:
        webp_filename = png_file.stem + ".webp"
        webp_path = output_path / webp_filename
        
        # Build FFmpeg command
        cmd = ["ffmpeg", "-y"]
        
        if use_gpu:
            # Add GPU acceleration options before input
            cmd.extend(["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"])
        
        cmd.extend(["-i", str(png_file)])
        
        # Add output options
        cmd.extend([
            "-c:v", "libwebp",
            "-quality", str(quality),
            "-compression_level", "6",
            str(webp_path)
        ])
        
        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, f"✓ Converted ({'GPU' if use_gpu else 'CPU'}): {png_file.name} -> {webp_filename}"
        else:
            return False, f"✗ FFmpeg error converting {png_file.name}: {result.stderr}"
            
    except Exception as e:
        return False, f"✗ Error converting {png_file.name}: {str(e)}"

def convert_single_png_pillow(png_file, output_path, quality, lossless):
    """Convert a single PNG file to WebP using Pillow."""
    try:
        # Open PNG image
        with Image.open(png_file) as img:
            # Create output filename
            webp_filename = png_file.stem + ".webp"
            webp_path = output_path / webp_filename
            
            # Save as WebP
            if lossless:
                img.save(webp_path, "WebP", lossless=True)
                return True, f"✓ Converted (lossless): {png_file.name} -> {webp_filename}"
            else:
                img.save(webp_path, "WebP", quality=quality, optimize=True)
                return True, f"✓ Converted (quality {quality}): {png_file.name} -> {webp_filename}"
                
    except Exception as e:
        return False, f"✗ Error converting {png_file.name}: {str(e)}"

def convert_png_to_webp_ffmpeg(input_folder, output_folder=None, quality=95, use_gpu=False, num_threads=1):
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return
    
    # Set output folder
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        # Create 'webp_output' folder in the same directory as input
        output_path = input_path / "webp_output"
        output_path.mkdir(exist_ok=True)
    
    # Find all PNG files
    png_files = list(input_path.glob("*.png")) + list(input_path.glob("*.PNG"))
    
    if not png_files:
        print(f"No PNG files found in '{input_folder}'")
        return
    
    print(f"Found {len(png_files)} PNG files to convert using FFmpeg...")
    print(f"Using {num_threads} thread(s) for processing")
    if use_gpu:
        print("GPU acceleration enabled (requires compatible hardware)")
    
    converted_count = 0
    thread_lock = threading.Lock()
    
    def process_and_print(png_file):
        nonlocal converted_count
        success, message = convert_single_png_ffmpeg(png_file, output_path, quality, use_gpu)
        
        with thread_lock:
            print(message)
            if success:
                converted_count += 1
        
        return success
    
    # Process files with thread pool
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_and_print, png_file) for png_file in png_files]
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                with thread_lock:
                    print(f"✗ Thread error: {str(e)}")
    
    print(f"\nFFmpeg conversion complete! {converted_count}/{len(png_files)} files converted successfully.")

def convert_png_to_webp(input_folder, output_folder=None, quality=95, lossless=False, num_threads=1):

    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return
    
    if not input_path.is_dir():
        print(f"Error: '{input_folder}' is not a directory.")
        return
    
    # Set output folder
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        # Create 'webp_output' folder in the same directory as input
        output_path = input_path / "webp_output"
        output_path.mkdir(exist_ok=True)
    
    # Find all PNG files
    png_files = list(input_path.glob("*.png")) + list(input_path.glob("*.PNG"))
    
    if not png_files:
        print(f"No PNG files found in '{input_folder}'")
        return
    
    print(f"Found {len(png_files)} PNG files to convert...")
    print(f"Using {num_threads} thread(s) for processing")
    converted_count = 0
    thread_lock = threading.Lock()
    
    def process_and_print(png_file):
        nonlocal converted_count
        success, message = convert_single_png_pillow(png_file, output_path, quality, lossless)
        
        with thread_lock:
            print(message)
            if success:
                converted_count += 1
        
        return success
    
    # Process files with thread pool
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_and_print, png_file) for png_file in png_files]
        
        # Wait for all tasks to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                with thread_lock:
                    print(f"✗ Thread error: {str(e)}")
    
    print(f"\nConversion complete! {converted_count}/{len(png_files)} files converted successfully.")

def main():
    parser = argparse.ArgumentParser(description="Convert PNG files to WebP format")
    parser.add_argument("input_folder", help="Path to folder containing PNG files")
    parser.add_argument("-o", "--output", help="Output folder (default: same as input)")
    parser.add_argument("-q", "--quality", type=int, default=95, 
                       help="WebP quality 0-100 (default: 95)")
    parser.add_argument("-l", "--lossless", action="store_true", 
                       help="Use lossless compression (ignores quality setting)")
    parser.add_argument("-t", "--threads", type=int, default=1,
                       help="Number of threads for parallel processing (default: 1)")
    parser.add_argument("--ffmpeg", action="store_true",
                       help="Use FFmpeg instead of Pillow for conversion")
    parser.add_argument("--gpu", action="store_true",
                       help="Enable GPU acceleration (requires FFmpeg and compatible GPU)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not 0 <= args.quality <= 100:
        print("Error: Quality must be between 0 and 100")
        sys.exit(1)
    
    if args.threads < 1:
        print("Error: Number of threads must be at least 1")
        sys.exit(1)
    
    if args.gpu and not args.ffmpeg:
        print("GPU acceleration requires --ffmpeg flag")
        sys.exit(1)
    
    # Warn about threading limitations with GPU
    if args.gpu and args.threads > 1:
        print("Warning: Using multiple threads with GPU acceleration may not improve performance")
        print("GPU processing is already highly parallel. Consider using 1-2 threads.")
    
    if args.ffmpeg:
        convert_png_to_webp_ffmpeg(
            input_folder=args.input_folder,
            output_folder=args.output,
            quality=args.quality,
            use_gpu=args.gpu,
            num_threads=args.threads
        )
    else:
        convert_png_to_webp(
            input_folder=args.input_folder,
            output_folder=args.output,
            quality=args.quality,
            lossless=args.lossless,
            num_threads=args.threads
        )

if __name__ == "__main__":
    main()
