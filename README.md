# Image similarity search using Perceptual Hashing
---
## Project Overview

This project explores how computer vision techniques can be applied to digital image collections. I wanted to apply technology to my personal photography portfolio composed of over 11,000 images in a way that helps me organize it efficiently. Searching for visual similarities across such a large archive would be very time consuming to do manually. This tool automates that process by finding patterns and connections.

---

## What This Project Does

1. Extracts metadata from images (dimensions, color statistics, visual characteristics)
2. Creates visual fingerprints using perceptual hashing (pHash)
3. Compares fingerprints to find visually similar images in a collection
4. Explains the results

---

## Why This Matters for Cultural Heritage

Museums, archives, and cultural institutions manage vast digital collections. Finding connections between objects is traditionally done manually by experts. Computational tools assist curators in discovering visual patterns, identify potential duplicates or related works across large archives and reveal unexpected connections that human eyes might miss.

This project is just a small-scale exploration of these ideas that still needs to be polished.

---

### What is a Hash?
Hashing is an umbrella term for techniques to create a short identifier for files on a computer system. Such files can be images, videos, music, Word documents, executables, or any other file on a computer system. A **perceptual hash (pHash)** is a fingerprint of a multimedia file derived from various features from its content. PHashes are "close" to one another if the features are similar, if some images have similarities to the human eye, t

### How pHash Works (Step by Step)

1. **Shrink the image** to a small standard size (e.g., 16x16 pixels)
2. **Convert to grayscale** - remove color information, keep structure
3. **Apply Discrete Cosine Transform (DCT)** - converts pixel values to frequency patterns
4. **Keep low frequencies** - these represent the overall structure, not fine details
5. **Compare each value to the average** - if above average, mark as 1; if below, mark as 0
6. **The result** is a string of 256 bits (0s and 1s), represented as hexadecimal

This process makes pHash:
- **Robust to scaling** - zooming in doesn't change the hash much
- **Robust to compression** - JPEG artifacts don't affect structure
- **Robust to color changes** - since it works in grayscale
- **Sensitive to composition** - the arrangement of shapes and light/dark areas

### Running the Metadata Explorer

To examine what information is contained in an image:
python analyze_image.py

text

Then choose:
- **Option 1**: Analyze a single image in detail
- **Option 2**: Analyze all images in a folder

Drag and drop your image or folder into the terminal when prompted.

### Running the Similarity Search

To find similar images in a collection:
python compare_images.py

text

You will be asked for:
1. A **reference image** - the image you want to find matches for
2. A **folder** - the collection to search through
3. **Number of results** - how many similar images to show

Drag and drop files/folders into the terminal when prompted.

---

## Example Workflow

### 1. Understand your reference image
python analyze_image.py
Choose option 1
Drag in: C:\Photos\landscape_reference.jpg

text

Output shows dimensions, color statistics, brightness, contrast, and the pHash fingerprint.

### 2. Understand your collection
python analyze_image.py
Choose option 2
Drag in: C:\Photos\italy_trip\

text

Output shows a summary of all images in the folder with their pHash values.

### 3. Find similar images
python compare_images.py
Reference: C:\Photos\landscape_reference.jpg
Folder: C:\Photos\italy_trip
Results: 10

text

Output shows the top 10 most similar images with distance scores and interpretations.

---

## Interpreting the Results

The program provides similarity assessments in plain language:

| Hash Distance | Interpretation | What It Means |
|---------------|----------------|---------------|
| 0 | IDENTICAL | Same exact image |
| 1-10 | EXTREMELY SIMILAR | Same scene, minimal changes (edited version, different compression) |
| 11-20 | VERY SIMILAR | Same subject, different angle or lighting |
| 21-30 | MODERATELY SIMILAR | Similar composition or subject type |
| 31-50 | SOMEWHAT SIMILAR | Shares some visual elements |
| 50+ | DIFFERENT | Different subjects and compositions |

---

## Limitations and Reflection

### What This Tool CAN Do
- Find images with similar overall structure and composition
- Work across different image sizes and compression levels
- Process hundreds of images quickly

### What This Tool CANNOT Do
- Recognize specific objects or people (no AI/ML)
- Understand semantic meaning or context
- Compare based on color palette (pHash works in grayscale)
- Replace human curatorial judgment

## Sources
https://www.phash.org/

