# Image similarity search using Perceptual Hashing
---
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
Hashing is an umbrella term for techniques to create a short identifier for files on a computer system. Such files can be images, videos, music, Word documents, executables, or any other file on a computer system. A **perceptual hash (pHash)** is a fingerprint of a multimedia file derived from various features from its content. PHashes are "close" to one another if the features are similar.

### Running the Metadata Explorer

To examine what information is contained in an image type "python analyze_image.py" in python.

Then choose bwtween 2 options:
- **Option 1**: Analyze a single image in detail
- **Option 2**: Analyze all images in a folder

Copy the path of your image or folder into the terminal when prompted.

To find similar images in a collection type "python compare_images.py"

You will be asked for:
1. A **reference image**: the image you want to find matches for
2. A **folder**: the collection to search through
3. **Number of results**: how many similar images to show

Copy the path of your image or folder into the terminal when prompted.

The output shows a summary of all images in the folder with their pHash values, for example the 10 most similar images with distance scores and interpretations.

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
I am aware of the current limitations of this project and I am to to improve the tool as I develop my coding skills.

### What This Tool can Do
- Find images with similar overall structure and composition
- Work across different image sizes and compression levels
- Process hundreds of images quickly

### What This Tool cannot Do
- Recognize specific objects or people (no AI)
- Understand semantic meaning or context
- Compare based on color palette (pHash works in grayscale)
- Analyse raw files


## Sources
https://pypi.org/project/ImageHash/
https://www.phash.org/
https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/online-research/other/perceptual-hashing-technology.pdf?v=328806
