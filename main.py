import os
import sys
from pathlib import Path
from PIL import Image
import argparse

def convert_png_to_webp(input_folder, output_folder=None, quality=95, lossless=False):
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
        output_path = input_path
    
    # Find all PNG files
    png_files = list(input_path.glob("*.png")) + list(input_path.glob("*.PNG"))
    
    if not png_files:
        print(f"No PNG files found in '{input_folder}'")
        return
    
    print(f"Found {len(png_files)} PNG files to convert...")
    converted_count = 0
    
    for png_file in png_files:
        try:
            # Open PNG image
            with Image.open(png_file) as img:
                # Convert RGBA to RGB if necessary (WebP supports both)
                # But for maximum compatibility, you might want to handle transparency
                
                # Create output filename
                webp_filename = png_file.stem + ".webp"
                webp_path = output_path / webp_filename
                
                # Save as WebP
                if lossless:
                    img.save(webp_path, "WebP", lossless=True)
                    print(f"Converted (lossless): {png_file.name} -> {webp_filename}")
                else:
                    img.save(webp_path, "WebP", quality=quality, optimize=True)
                    print(f"Converted (quality {quality}): {png_file.name} -> {webp_filename}")
                
                converted_count += 1
                
        except Exception as e:
            print(f"✗ Error converting {png_file.name}: {str(e)}")
    
    print(f"\nConversion complete! {converted_count}/{len(png_files)} files converted successfully.")

def main():
    parser = argparse.ArgumentParser(description="Convert PNG files to WebP format")
    parser.add_argument("input_folder", help="Path to folder containing PNG files")
    parser.add_argument("-o", "--output", help="Output folder (default: same as input)")
    parser.add_argument("-q", "--quality", type=int, default=95, 
                       help="WebP quality 0-100 (default: 95)")
    parser.add_argument("-l", "--lossless", action="store_true", 
                       help="Use lossless compression (ignores quality setting)")
    
    args = parser.parse_args()
    
    # Validate quality
    if not 0 <= args.quality <= 100:
        print("Error: Quality must be between 0 and 100")
        sys.exit(1)
    
    convert_png_to_webp(
        input_folder=args.input_folder,
        output_folder=args.output,
        quality=args.quality,
        lossless=args.lossless
    )

if __name__ == "__main__":
    main()