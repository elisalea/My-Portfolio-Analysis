# Image Similarity Search using Perceptual Hashing

## A Digital Humanities Approach to Visual Archives

---

## Project Overview

This project explores how computer vision techniques can be applied to digital image collections. It was developed as part of an application for the **DHDK (Digital Humanities and Digital Knowledge)** program, building on a background in **DAMS (Discipline delle Arti, della Musica e dello Spettacolo)** .

The goal is not to demonstrate advanced programming skills, but rather to show:
- **Curiosity** about how computational methods can enhance humanities research
- **Understanding** of what happens when we analyze images digitally
- **Documentation** skills essential for digital humanities projects

---

## The Core Question

**How can a computer "see" similarity between images?**

When we look at two photos, we instinctively know if they're similar. But a computer sees only numbers - pixel values, color channels, mathematical patterns. This project explores how to translate human visual intuition into computational methods.

---

## What This Project Does

1. **Extracts metadata** from images (dimensions, color statistics, visual characteristics)
2. **Creates visual fingerprints** using perceptual hashing (pHash)
3. **Compares fingerprints** to find visually similar images in a collection
4. **Explains the results** in human-readable terms

---

## Why This Matters for Cultural Heritage

Museums, archives, and cultural institutions manage vast digital collections. Finding connections between objects is traditionally done manually by experts. Computational tools can:

- **Assist** (not replace) curators in discovering visual patterns
- **Identify** potential duplicates or related works across large archives
- **Reveal** unexpected connections that human eyes might miss
- **Document** visual characteristics in a systematic, reproducible way

This project is a small-scale exploration of these ideas, applied to a personal photo collection.

---

## How It Works: Perceptual Hashing Explained

### What is a Hash?
A hash is a fixed-length code generated from data. In cryptography, changing even one bit of input completely changes the hash. This is good for security but useless for finding similar images.

### What is a Perceptual Hash?
A **perceptual hash (pHash)** is different. It's designed so that **similar inputs produce similar hashes**. If two images look alike to a human, their pHash values will be close together.

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

### How Comparison Works

The **Hamming distance** between two hashes is the number of bits that differ:
