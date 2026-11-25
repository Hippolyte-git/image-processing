# Automated Image Analysis Pipeline & Interactive Toolbox

Mini-project developed for the **Image Analysis and Processing** Master's course at **École des Mines de Saint-Étienne**.

## Overview

This project provides two complementary interfaces for classical image analysis designed to be accessible to non-specialists (e.g., biologists analyzing microscopy images):

1. **Automated Pipeline & PDF Report Generator (`image_analysis_pipeline.ipynb`)**
   - Automatically detects whether the input image is **RGB color**, **grayscale**, or **binary**.
   - Routes the image through a tailored **6-stage processing pipeline**:
     - *Color (RGB):* RGB histograms → per-channel median denoising → HSV value-channel equalization → Otsu thresholding → morphological opening → Sobel edge detection.
     - *Grayscale:* Intensity histogram → median denoising → histogram equalization → Otsu thresholding → morphological opening → Sobel edge detection.
     - *Binary:* Foreground/background pixel ratio → morphological closing → dilation → skeletonization → morphological opening → Sobel boundary extraction.
   - Exports a clean **3-page landscape A4 PDF report** with annotated visuals and plain-language captions.

2. **Interactive Streamlit Web App (`app.py`)**
   - Upload any image (`.png`, `.jpg`, `.bmp`, `.tif`), adjust filter parameters interactively in the sidebar, and inspect before/after comparisons for all 6 pipeline stages in real time.

## Quickstart

### Run the Interactive Web App
```bash
streamlit run project/app.py
```

### Run the Automated Pipeline Notebook
Open `project/image_analysis_pipeline.ipynb` in Jupyter / VS Code and run all cells. By default, it processes `project/sample_image.png` and outputs `report_sample_image.pdf`.
