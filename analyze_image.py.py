"""
IMAGE METADATA EXPLORER
------------------------
This script extracts and explains all the visual metadata from an image.
It shows exactly what information the computer "sees" when analyzing a photo,
including the perceptual hash that will be used for similarity comparison.

This is Step 1 of the project: understanding what makes an image unique
before we compare it to others.
"""

import os
from pathlib import Path
from PIL import Image, ImageStat
import imagehash


def analyze_single_image(image_path):
    """
    Extract and explain all metadata from a single image.
    """
    print("=" * 70)
    print("  IMAGE METADATA EXPLORER")
    print("=" * 70)
    print()
    
    # Basic file information
    file_name = os.path.basename(image_path)
    file_size = os.path.getsize(image_path)
    file_size_kb = file_size / 1024
    file_size_mb = file_size_kb / 1024
    
    print(f"FILE INFORMATION")
    print(f"-" * 70)
    print(f"  File name:        {file_name}")
    print(f"  File path:        {image_path}")
    print(f"  File size:        {file_size:,} bytes ({file_size_kb:.1f} KB / {file_size_mb:.2f} MB)")
    print()
    
    # Open the image
    img = Image.open(image_path)
    
    # Image dimensions
    width, height = img.size
    total_pixels = width * height
    aspect_ratio = width / height
    
    print(f"IMAGE DIMENSIONS")
    print(f"-" * 70)
    print(f"  Width:            {width} pixels")
    print(f"  Height:           {height} pixels")
    print(f"  Total pixels:     {total_pixels:,} ({total_pixels / 1_000_000:.1f} megapixels)")
    print(f"  Aspect ratio:     {aspect_ratio:.2f}:1 ({'landscape' if aspect_ratio > 1 else 'portrait' if aspect_ratio < 1 else 'square'})")
    print()
    
    # Image mode and color information
    print(f"COLOR INFORMATION")
    print(f"-" * 70)
    print(f"  Color mode:       {img.mode}")
    
    # Explain what the mode means
    mode_explanations = {
        "RGB": "Red, Green, Blue - Standard color image with 3 color channels",
        "RGBA": "RGB + Alpha (transparency) - 4 channels",
        "L": "Grayscale - Single channel, black and white",
        "CMYK": "Cyan, Magenta, Yellow, Black - Used for printing",
        "HSV": "Hue, Saturation, Value - Perceptual color space",
    }
    if img.mode in mode_explanations:
        print(f"  Mode meaning:     {mode_explanations[img.mode]}")
    print()
    
    # Convert to RGB if needed for analysis
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Statistical color analysis
    stats = ImageStat.Stat(img)
    
    print(f"COLOR STATISTICS (RGB Channels)")
    print(f"-" * 70)
    
    channel_names = ["Red", "Green", "Blue"]
    for i, name in enumerate(channel_names):
        mean_val = stats.mean[i]
        median_val = stats.median[i]
        stddev_val = stats.stddev[i]
        print(f"  {name} channel:")
        print(f"    Average value:  {mean_val:.1f} (out of 255)")
        print(f"    Median value:   {median_val:.1f}")
        print(f"    Variability:    {stddev_val:.1f} (higher = more contrast in this color)")
    
    print()
    
    # Overall brightness and contrast
    overall_brightness = sum(stats.mean) / (3 * 255)
    overall_contrast = sum(stats.stddev) / (3 * 128)
    
    print(f"OVERALL IMAGE CHARACTERISTICS")
    print(f"-" * 70)
    print(f"  Brightness:       {overall_brightness:.1%} ({'dark' if overall_brightness < 0.3 else 'balanced' if overall_brightness < 0.7 else 'bright'})")
    print(f"  Contrast:         {overall_contrast:.1%} ({'flat' if overall_contrast < 0.2 else 'normal' if overall_contrast < 0.5 else 'high contrast'})")
    print()
    
    # Perceptual hash - the "visual fingerprint"
    print(f"PERCEPTUAL HASH (pHash) - The Visual Fingerprint")
    print(f"-" * 70)
    print(f"  What is pHash?")
    print(f"    A perceptual hash is a 'fingerprint' of the image's visual structure.")
    print(f"    It converts the image into a short code based on patterns of light")
    print(f"    and dark areas, not exact pixel colors.")
    print(f"    ")
    print(f"    Two photos of the same scene will have SIMILAR hashes")
    print(f"    even if one is brighter, darker, or slightly zoomed.")
    print(f"    Two completely different scenes will have DIFFERENT hashes.")
    print()
    
    # Compute the hash
    phash = imagehash.phash(img, hash_size=16)
    print(f"  pHash value:      {phash}")
    print(f"  Hash size:        16x16 = 256 bits")
    print(f"  Format:           Hexadecimal (each character = 4 bits)")
    print()
    
    # Additional hash types for comparison
    print(f"OTHER HASH TYPES (for reference)")
    print(f"-" * 70)
    
    ahash = imagehash.average_hash(img)
    dhash = imagehash.dhash(img)
    
    print(f"  Average Hash:     {ahash}")
    print(f"    (Simpler, faster, less accurate - compares average brightness)")
    print(f"  Difference Hash:  {dhash}")
    print(f"    (Focuses on edges and gradients between pixels)")
    print()
    
    print(f"SUMMARY")
    print(f"-" * 70)
    print(f"  This image is a {width}x{height} {img.mode} image.")
    print(f"  Its visual fingerprint (pHash) is: {phash}")
    print(f"  This fingerprint will be used to find similar images.")
    print()
    print("=" * 70)
    
    return {
        "file_name": file_name,
        "width": width,
        "height": height,
        "mode": img.mode,
        "brightness": overall_brightness,
        "contrast": overall_contrast,
        "phash": str(phash)
    }


def analyze_folder(folder_path):
    """
    Analyze all images in a folder and show their metadata.
    """
    print("=" * 70)
    print("  FOLDER ANALYSIS: All Images")
    print("=" * 70)
    print()
    
    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    all_images = []
    
    for ext in extensions:
        all_images.extend(Path(folder_path).rglob(f"*{ext}"))
        all_images.extend(Path(folder_path).rglob(f"*{ext.upper()}"))
    
    # Remove duplicates
    all_images = list(set(all_images))
    
    print(f"  Images found:     {len(all_images)}")
    print()
    
    if len(all_images) == 0:
        print("  No images found in this folder.")
        return []
    
    all_data = []
    
    for i, img_path in enumerate(all_images, 1):
        print(f"  [{i}/{len(all_images)}] {img_path.name}")
        print(f"       Path: {img_path}")
        
        try:
            img = Image.open(img_path)
            w, h = img.size
            phash = imagehash.phash(img.convert('RGB') if img.mode != 'RGB' else img, hash_size=16)
            
            print(f"       Size: {w}x{h} | pHash: {phash}")
            
            all_data.append({
                "path": str(img_path),
                "name": img_path.name,
                "width": w,
                "height": h,
                "phash": str(phash),
                "phash_obj": phash
            })
        except Exception as e:
            print(f"       ERROR: Could not process - {e}")
        
        print()
    
    print("=" * 70)
    return all_data


def main():
    """
    Main program - asks user what they want to analyze.
    """
    print()
    print("What would you like to analyze?")
    print("  1. A single image (detailed metadata)")
    print("  2. A folder of images (summary metadata)")
    print()
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        image_path = input("\nDrag your image here: ").strip().strip('"')
        if os.path.exists(image_path):
            analyze_single_image(image_path)
        else:
            print("File not found!")
    
    elif choice == "2":
        folder_path = input("\nDrag your folder here: ").strip().strip('"')
        if os.path.exists(folder_path):
            analyze_folder(folder_path)
        else:
            print("Folder not found!")
    
    else:
        print("Invalid choice!")
    
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
