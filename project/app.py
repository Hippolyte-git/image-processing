"""
Interactive Image Analysis Toolbox (Streamlit Web App)

Applies a 6-stage classical image processing pipeline to any uploaded image:
1. Intensity histogram analysis
2. Median filtering (denoising)
3. Histogram equalization (contrast enhancement)
4. Otsu automatic thresholding (binarization)
5. Morphological opening (artifact removal)
6. Sobel edge detection
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import skimage.color
import skimage.exposure
import skimage.filters
import skimage.morphology
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Image Analysis Toolbox",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_and_preprocess_image(uploaded_file):
    """Load an uploaded image as a NumPy array and produce an 8-bit grayscale version."""
    img_pil = Image.open(uploaded_file)
    img_raw = np.array(img_pil)

    if img_raw.ndim >= 3:
        img_gray = (skimage.color.rgb2gray(img_raw[..., :3]) * 255).astype(np.uint8)
    else:
        img_gray = img_raw.astype(np.uint8)

    return img_raw, img_gray


def plot_intensity_histogram(img_gray: np.ndarray):
    """Stage 1: Compute and plot the grayscale intensity histogram."""
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.hist(img_gray.ravel(), bins=256, range=(0, 256), color="black", alpha=0.75)
    ax.set_title("Intensity Histogram", fontsize=10)
    ax.set_xlabel("Pixel Intensity (0–255)")
    ax.set_ylabel("Pixel Count")
    ax.grid(alpha=0.3)
    return fig


def apply_median_filter(img_gray: np.ndarray, size: int = 3) -> np.ndarray:
    """Stage 2: Denoise with a square median filter."""
    return scipy.ndimage.median_filter(img_gray, size=size)


def apply_histogram_equalization(img_filtered: np.ndarray) -> np.ndarray:
    """Stage 3: Global contrast enhancement via histogram equalization."""
    img_eq = skimage.exposure.equalize_hist(img_filtered)
    return (img_eq * 255).astype(np.uint8)


def apply_otsu_thresholding(img_eq: np.ndarray):
    """Stage 4: Automatic foreground/background binarization using Otsu's method."""
    threshold = skimage.filters.threshold_otsu(img_eq)
    return img_eq > threshold, threshold


def apply_morphological_opening(img_binary: np.ndarray, radius: int = 2) -> np.ndarray:
    """Stage 5: Remove isolated foreground artifacts via morphological opening."""
    selem = skimage.morphology.disk(radius)
    return skimage.morphology.opening(img_binary, selem)


def apply_sobel_edges(img_eq: np.ndarray) -> np.ndarray:
    """Stage 6: Highlight object boundaries with the Sobel gradient magnitude."""
    return skimage.filters.sobel(img_eq)


# -----------------------------------------------------------------------------
# Main Application UI
# -----------------------------------------------------------------------------
st.title("Image Analysis Toolbox")
st.markdown(
    "Upload any image to run an interactive **6-stage classical image processing pipeline** "
    "with side-by-side comparisons at every step."
)

with st.sidebar:
    st.header("1. Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image", type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"]
    )

    st.header("2. Parameters")
    median_size = st.slider("Median Filter Kernel Size", min_value=3, max_value=9, value=3, step=2)
    disk_radius = st.slider("Morphological Disk Radius", min_value=1, max_value=8, value=2, step=1)

    if uploaded_file is not None:
        img_raw, img_gray = load_and_preprocess_image(uploaded_file)

        st.header("Image Summary")
        st.write(f"**Dimensions:** {img_raw.shape[0]} x {img_raw.shape[1]} px")
        st.write(f"**Original Channels:** {img_raw.shape[2] if img_raw.ndim >= 3 else 1}")
        st.write(f"**Data Type:** `{img_raw.dtype}`")
        st.write(f"**Grayscale Min / Max:** {img_gray.min()} / {img_gray.max()}")
        st.image(img_raw, caption="Original Image", use_container_width=True)

if uploaded_file is not None:
    st.divider()
    st.header("Processing Pipeline")

    # Stage 1: Histogram
    st.subheader("1. Intensity Histogram Analysis")
    st.info("Displays the distribution of pixel intensities to diagnose low contrast or clipping.")
    st.pyplot(plot_intensity_histogram(img_gray))

    # Stage 2: Median Filtering
    st.divider()
    st.subheader("2. Median Filtering (Denoising)")
    st.info("Suppresses impulse and sensor noise while preserving sharp object edges.")
    img_filtered = apply_median_filter(img_gray, size=median_size)
    col1, col2 = st.columns(2)
    with col1:
        st.image(img_gray, caption="Before: Grayscale", use_container_width=True, clamp=True)
    with col2:
        st.image(
            img_filtered,
            caption=f"After: Median Filter ({median_size}x{median_size})",
            use_container_width=True,
            clamp=True,
        )

    # Stage 3: Histogram Equalization
    st.divider()
    st.subheader("3. Histogram Equalization (Contrast Enhancement)")
    st.info("Redistributes intensity levels uniformly to improve global contrast before segmentation.")
    img_eq = apply_histogram_equalization(img_filtered)
    col1, col2 = st.columns(2)
    with col1:
        st.image(img_filtered, caption="Before: Denoised", use_container_width=True, clamp=True)
    with col2:
        st.image(img_eq, caption="After: Histogram Equalization", use_container_width=True, clamp=True)

    # Stage 4: Otsu Thresholding
    st.divider()
    st.subheader("4. Otsu Thresholding (Binarization)")
    img_binary, otsu_thresh = apply_otsu_thresholding(img_eq)
    st.info(
        f"Automatically separates foreground from background by maximizing inter-class variance. "
        f"Computed optimal threshold: **{otsu_thresh:.1f} / 255**."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.image(img_eq, caption="Before: Equalized", use_container_width=True, clamp=True)
    with col2:
        st.image(img_binary.astype(float), caption="After: Binary Mask", use_container_width=True, clamp=True)

    # Stage 5: Morphological Opening
    st.divider()
    st.subheader("5. Morphological Opening (Artifact Removal)")
    st.info("Removes small isolated foreground speckles introduced during binarization.")
    img_opened = apply_morphological_opening(img_binary, radius=disk_radius)
    col1, col2 = st.columns(2)
    with col1:
        st.image(img_binary.astype(float), caption="Before: Raw Binary Mask", use_container_width=True, clamp=True)
    with col2:
        st.image(
            img_opened.astype(float),
            caption=f"After: Morphological Opening (disk r={disk_radius})",
            use_container_width=True,
            clamp=True,
        )

    # Stage 6: Sobel Edge Detection
    st.divider()
    st.subheader("6. Edge Detection (Sobel Filter)")
    st.info("Highlights sharp spatial intensity transitions corresponding to object boundaries.")
    img_sobel = apply_sobel_edges(img_eq)
    st.image(img_sobel, caption="Result: Sobel Gradient Magnitude", use_container_width=True, clamp=True)

else:
    st.info("Upload an image using the left sidebar to launch the analysis pipeline.")
