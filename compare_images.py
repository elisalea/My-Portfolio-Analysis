"""
IMAGE SIMILARITY COMPARATOR
----------------------------
This script compares a reference image to all images in a folder using
perceptual hashing (pHash). It shows detailed comparison metrics and
explains why images are considered similar or different.

This is Step 3 of the project: using the pHash fingerprints to find
visually similar images in a collection.
"""

import os
from pathlib import Path
from PIL import Image
import imagehash


def compare_images(reference_path, folder_path, top_n=10):
    """
    Compare a reference image to all images in a folder.
    Returns the most similar ones with detailed explanations.
    """
    
    print("=" * 70)
    print("  IMAGE SIMILARITY SEARCH")
    print("  Using Perceptual Hashing (pHash)")
    print("=" * 70)
    print()
    
    # --- REFERENCE IMAGE ANALYSIS ---
    print("STEP 1: Analyze Reference Image")
    print("-" * 70)
    
    ref_img = Image.open(reference_path)
    if ref_img.mode != 'RGB':
        ref_img = ref_img.convert('RGB')
    
    ref_name = os.path.basename(reference_path)
    ref_width, ref_height = ref_img.size
    ref_phash = imagehash.phash(ref_img, hash_size=16)
    
    print(f"  Reference image:  {ref_name}")
    print(f"  Dimensions:       {ref_width} x {ref_height}")
    print(f"  pHash fingerprint: {ref_phash}")
    print()
    
    # --- LOAD DATABASE IMAGES ---
    print("STEP 2: Load Image Database")
    print("-" * 70)
    
    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    all_images = []
    
    for ext in extensions:
        all_images.extend(Path(folder_path).rglob(f"*{ext}"))
        all_images.extend(Path(folder_path).rglob(f"*{ext.upper()}"))
    
    all_images = list(set(all_images))
    
    # Remove the reference image from the list if present
    all_images = [img for img in all_images 
                  if str(img.absolute()) != os.path.abspath(reference_path)]
    
    print(f"  Images in folder: {len(all_images)}")
    print(f"  (Reference image excluded from comparison)")
    print()
    
    if len(all_images) == 0:
        print("  No other images found to compare.")
        return []
    
    # --- COMPUTE ALL HASHES AND COMPARE ---
    print("STEP 3: Compute pHash for All Images and Compare")
    print("-" * 70)
    print(f"  Processing {len(all_images)} images...")
    print()
    
    results = []
    
    for i, img_path in enumerate(all_images):
        try:
            # Show progress every 10 images
            if (i + 1) % 10 == 0 or i == 0:
                print(f"  Progress: {i+1}/{len(all_images)}")
            
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_hash = imagehash.phash(img, hash_size=16)
            distance = abs(ref_phash - img_hash)
            
            # Calculate similarity percentage
            max_possible_distance = 256  # 16x16 hash = 256 bits
            similarity = ((max_possible_distance - distance) / max_possible_distance) * 100
            
            results.append({
                "path": str(img_path),
                "name": img_path.name,
                "width": img.width,
                "height": img.height,
                "phash": str(img_hash),
                "distance": distance,
                "similarity": similarity
            })
            
        except Exception as e:
            print(f"  Could not process: {img_path.name} - {e}")
    
    print()
    print(f"  Successfully processed: {len(results)} images")
    print()
    
    # --- SORT AND DISPLAY RESULTS ---
    results.sort(key=lambda x: x["distance"])
    
    print("STEP 4: Results - Most Similar Images")
    print("=" * 70)
    print()
    print(f"  Distance Scale:")
    print(f"    0      = Identical images (same pHash)")
    print(f"    1-10   = Extremely similar (same scene, minor changes)")
    print(f"    11-20  = Very similar (same subject, different angle/light)")
    print(f"    21-30  = Moderately similar (similar type of photo)")
    print(f"    31-50  = Somewhat similar (shared visual elements)")
    print(f"    50+    = Different images")
    print()
    print("-" * 70)
    print()
    
    for i, result in enumerate(results[:top_n], 1):
        distance = result["distance"]
        similarity = result["similarity"]
        
        # Interpret the similarity
        if distance == 0:
            interpretation = "IDENTICAL - Same image or exact copy"
        elif distance <= 10:
            interpretation = "EXTREMELY SIMILAR - Same scene, minimal differences"
        elif distance <= 20:
            interpretation = "VERY SIMILAR - Same subject, slightly different shot"
        elif distance <= 30:
            interpretation = "MODERATELY SIMILAR - Similar composition or subject type"
        elif distance <= 50:
            interpretation = "SOMEWHAT SIMILAR - Shares some visual characteristics"
        else:
            interpretation = "DIFFERENT - Different subjects and composition"
        
        print(f"  #{i} - {result['name']}")
        print(f"       File path:    {result['path']}")
        print(f"       Dimensions:   {result['width']} x {result['height']}")
        print(f"       pHash:        {result['phash']}")
        print(f"       Hash distance: {distance}")
        print(f"       Similarity:   {similarity:.1f}%")
        print(f"       Assessment:   {interpretation}")
        print()
    
    # --- SUMMARY ---
    print("=" * 70)
    print("  SUMMARY")
    print("-" * 70)
    
    if len(results) > 0:
        avg_distance = sum(r["distance"] for r in results) / len(results)
        best_match = results[0]
        
        print(f"  Total images compared: {len(results)}")
        print(f"  Average hash distance:  {avg_distance:.1f}")
        print(f"  Best match:             {best_match['name']}")
        print(f"  Best match distance:    {best_match['distance']}")
        print(f"  Best match similarity:  {best_match['similarity']:.1f}%")
    else:
        print("  No valid comparisons made.")
    
    print()
    print("=" * 70)
    
    return results


def main():
    """
    Main program - guides the user through comparison.
    """
    print()
    print("IMAGE SIMILARITY COMPARISON TOOL")
    print()
    
    reference_path = input("Drag your REFERENCE image here: ").strip().strip('"')
    if not os.path.exists(reference_path):
        print("Reference image not found!")
        input("\nPress Enter to close...")
        return
    
    folder_path = input("Drag your FOLDER of images here: ").strip().strip('"')
    if not os.path.exists(folder_path):
        print("Folder not found!")
        input("\nPress Enter to close...")
        return
    
    top_n = input("How many similar images to show? (default 10): ").strip()
    if top_n == "":
        top_n = 10
    else:
        top_n = int(top_n)
    
    print()
    compare_images(reference_path, folder_path, top_n)
    
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
    
