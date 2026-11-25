# Image Processing & Analysis

A collection of hands-on laboratory notebooks and an end-to-end image analysis mini-project developed during the **Image Analysis and Processing** Master's course at **École des Mines de Saint-Étienne**.

The repository covers classical and mathematical image processing—from low-level intensity transforms and Fourier analysis to astronomical deconvolution (Hubble Space Telescope FITS data), morphological segmentation, from-scratch connected component labeling, integral-geometry shape descriptors, and an interactive Streamlit web application.

---

## Repository Structure

```text
.
├── labs/
│   ├── 01_fundamentals_filtering_fft.ipynb          # Histograms, contrast stretching, spatial filters, 2D FFT
│   ├── 02_intensity_transformations.ipynb           # Gamma correction, sigmoid stretching, LUT equalization & matching
│   ├── 03_noise_modeling_denoising.ipynb            # Noise distributions & spatial filter denoising (PSNR)
│   ├── 04_image_deconvolution.ipynb                 # Inverse, Wiener, Van Cittert, Richardson-Lucy & Hubble FITS
│   ├── 05_thresholding_kmeans_segmentation.ipynb    # Otsu, iterative thresholding & 3D RGB K-Means clustering
│   ├── 06_morphological_segmentation_watershed.ipynb# Ovarian follicle histology & distance-transform watershed
│   ├── 07_connected_component_labeling.ipynb        # Two-pass 8-connected CCL implemented from scratch
│   ├── 08_shape_descriptors_diagrams.ipynb          # Crofton perimeter, Feret diameters & Kimia shape diagrams
│   └── psf_motion.npy                               # Motion-blur Point Spread Function used in Lab 04
├── project/
│   ├── app.py                                       # Interactive Streamlit web app (6-stage processing pipeline)
│   ├── image_analysis_pipeline.ipynb                # Auto-detecting RGB/grayscale/binary pipeline + PDF report generator
│   ├── sample_image.png                             # Sample input image for out-of-the-box execution
│   └── README.md                                    # Mini-project documentation
├── Images/                                          # Biomedical, astronomical (FITS), Kimia-99 & test datasets
├── requirements.txt
└── README.md
```

---

## Laboratory Notebooks

| # | Notebook | Key Concepts & Algorithms | Datasets |
|---|----------|---------------------------|----------|
| 01 | [Fundamentals, Filtering & 2D FFT](labs/01_fundamentals_filtering_fft.ipynb) | Custom histogram (`np.bincount`), affine contrast stretching, rank & Gaussian filters, 2D FFT amplitude/phase spectra | Muscle, cornea cells, blood cells, retina |
| 02 | [Intensity Transformations](labs/02_intensity_transformations.ipynb) | Gamma correction, sigmoid contrast stretching, custom LUT histogram equalization & histogram matching | Osteoblast microscopy |
| 03 | [Noise Modeling & Denoising](labs/03_noise_modeling_denoising.ipynb) | Uniform, Gaussian, Salt & Pepper, and Exponential noise simulation; spatial filter benchmarking with PSNR | Standard `camera` benchmark |
| 04 | [Image Restoration & Deconvolution](labs/04_image_deconvolution.ipynb) | Motion PSF/OTF modeling, Inverse filter, Wiener filter, Van Cittert (VCA), Richardson-Lucy (RLA), Unsupervised Wiener | Checkerboard, **Hubble Space Telescope** FITS (Jupiter & Saturn) |
| 05 | [Thresholding & K-Means Segmentation](labs/05_thresholding_kmeans_segmentation.ipynb) | Otsu thresholding, Ridler-Calvard iterative thresholding from scratch, 2D & 3D RGB K-Means clustering | Microscopy cells, RGB test image |
| 06 | [Morphological Segmentation & Watershed](labs/06_morphological_segmentation_watershed.ipynb) | Channel thresholding, binary dilation/hole-filling, Euclidean distance transform, morphological regional maxima, Watershed | Ovarian follicle histology, overlapping circles |
| 07 | [Connected Component Labeling](labs/07_connected_component_labeling.ipynb) | Two-pass 8-connectivity CCL with transitive equivalence merging from scratch, benchmarked against `scikit-image` | Synthetic Gaussian blobs |
| 08 | [Shape Descriptors & Shape Diagrams](labs/08_shape_descriptors_diagrams.ipynb) | Discrete Crofton perimeter, Feret diameters, inscribed circle radius, Blaschke/Santaló shape diagrams & K-Means evaluation | Kimia-99 (`apple`, `Bone`, `camel`) |

---

## Mini-Project: Image Analysis Toolbox

Located in [`project/`](project/README.md), this mini-project packages classical image analysis workflows into two ready-to-use tools:

1. **Interactive Streamlit Web App (`project/app.py`)** — Upload any image, tune median-filter and morphological structuring-element parameters interactively, and inspect before/after results across all 6 stages (histogram, median denoising, histogram equalization, Otsu binarization, morphological opening, and Sobel edge detection).
2. **Automated Modality-Aware Pipeline (`project/image_analysis_pipeline.ipynb`)** — Automatically detects whether an image is **RGB color**, **grayscale**, or **binary**, applies a dedicated 6-stage pipeline, and exports a formatted **3-page landscape A4 PDF report**.

---

## Getting Started

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/Hippolyte-git/image-processing.git
cd image-processing
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Lab Notebooks

```bash
jupyter lab
```
Open any notebook in `labs/` or `project/image_analysis_pipeline.ipynb` and run all cells. All image paths are relative to the repository layout and work cross-platform.

### 3. Launch the Interactive Web App

```bash
streamlit run project/app.py
```

---

## Tech Stack

- **Core Scientific Python:** NumPy, SciPy, Matplotlib
- **Image Processing & Vision:** scikit-image, imageio, Pillow
- **Machine Learning:** scikit-learn (K-Means clustering)
- **Astronomy Data:** Astropy (FITS I/O)
- **Web Interface:** Streamlit

---

## Author

**Hippolyte Valentin** — École des Mines de Saint-Étienne
