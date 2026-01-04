# Selective Halftone Implementation Guide

## Overview

This implementation allows you to apply halftone effects **only to the subject** while preserving the original background quality. This creates a striking visual effect similar to the sample images you provided.

## Key Features

1. **Multiple Segmentation Methods** - Choose the best method for your use case
2. **Integration with Existing Code** - Uses your existing halftone generation functions
3. **Smooth Blending** - Advanced mask refinement for seamless transitions
4. **Quality Preservation** - Maintains background quality while applying effect to subject

## Installation

### Required (Already Installed)
- `opencv-python`
- `Pillow`
- `numpy`
- `scikit-image`
- `matplotlib`

### Optional (Recommended for Best Results)

**REMBG** (Best Quality - Recommended):
```bash
pip install rembg
```
- Uses U2Net deep learning model
- Works for any subject (people, objects, animals)
- Very accurate segmentation
- Handles complex backgrounds

**MediaPipe** (Best for People/Portraits):
```bash
pip install mediapipe
```
- Optimized for person segmentation
- Very fast, real-time capable
- Great for portraits
- May not work well for non-people subjects

## Segmentation Methods Comparison

| Method | Quality | Speed | Best For | Dependencies |
|--------|---------|-------|----------|--------------|
| **REMBG** | ⭐⭐⭐⭐⭐ | Medium | Any subject | `pip install rembg` |
| **MediaPipe** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | People/Portraits | `pip install mediapipe` |
| **GrabCut** | ⭐⭐⭐ | Medium | General use | Built-in (OpenCV) |
| **Saliency** | ⭐⭐ | Fast | High contrast | Built-in (OpenCV) |
| **Simple** | ⭐ | Fast | Fallback only | Built-in |

## Usage

### Basic Usage

```python
from selective_halftone import selective_halftone_pipeline, visualize_results

# Process image with REMBG (best quality)
original, mask, halftone, result = selective_halftone_pipeline(
    'path/to/image.jpg',
    mask_method='rembg',  # or 'mediapipe', 'grabcut', 'saliency', 'simple'
    cell_size=12,
    max_radius=7,
    bg_color=(255, 255, 255),  # White background
    dot_color=(0, 0, 0)        # Black dots
)

# Visualize results
visualize_results(original, mask, halftone, result)
```

### Method Selection Guide

**For Best Quality (Any Subject):**
```python
result = selective_halftone_pipeline(
    'image.jpg',
    mask_method='rembg'  # Install: pip install rembg
)
```

**For People/Portraits (Fast):**
```python
result = selective_halftone_pipeline(
    'portrait.jpg',
    mask_method='mediapipe'  # Install: pip install mediapipe
)
```

**For General Use (No Extra Dependencies):**
```python
result = selective_halftone_pipeline(
    'image.jpg',
    mask_method='grabcut'  # Built into OpenCV
)
```

## How It Works

### 1. Subject Segmentation
- Detects and isolates the subject from the background
- Creates a binary mask (1 = subject, 0 = background)
- Multiple methods available for different use cases

### 2. Mask Refinement
- Smooths mask edges with morphological operations
- Applies Gaussian blur for soft transitions (feathering)
- Prevents harsh edges in final result

### 3. Halftone Generation
- Uses your existing `generate_classic_halftone()` function
- Applies halftone effect to the entire image
- Maintains quality and consistency with your existing pipeline

### 4. Selective Blending
- Blends halftone (subject) with original (background)
- Uses alpha blending for smooth transitions
- Formula: `result = original * (1 - mask) + halftone * mask`

## Integration with Main Pipeline

To integrate this into your main CLI (`src/main.py`), you would:

1. Add a `--selective` flag
2. Import the selective halftone functions
3. Modify the pipeline to:
   - Generate mask
   - Apply halftone to full image
   - Blend selectively

Example integration:
```python
if args.selective:
    from core.selective_halftone import selective_halftone_pipeline
    # Use selective pipeline instead of regular
```

## Advanced Options

### Custom Mask Refinement
```python
mask_refined = refine_mask(
    mask,
    iterations=3,      # More = smoother but may lose detail
    blur_size=15,      # Larger = softer edges
    edge_feather=True  # Enable soft transitions
)
```

### Custom GrabCut Rectangle
```python
# Manually specify subject bounding box
rect = (x, y, width, height)
mask = create_subject_mask_grabcut(image, rect=rect, iterations=10)
```

## Troubleshooting

### REMBG Not Working
- Ensure you have internet connection (first run downloads model)
- Check: `pip install rembg[new]` for latest version
- Model downloads to `~/.u2net/` on first use

### MediaPipe Not Detecting Person
- MediaPipe is optimized for people/selfies
- Try REMBG for other subjects
- Ensure person is clearly visible and centered

### Poor Mask Quality
- Try different segmentation methods
- Adjust mask refinement parameters
- For GrabCut: manually specify better bounding box
- For REMBG: ensure good lighting and contrast

### Blending Artifacts
- Increase `blur_size` in `refine_mask()`
- Adjust `iterations` for smoother mask
- Check mask coverage (should be reasonable, not too small/large)

## Performance Notes

- **REMBG**: ~2-5 seconds per image (first run slower due to model download)
- **MediaPipe**: ~0.1-0.5 seconds per image (very fast)
- **GrabCut**: ~0.5-2 seconds per image (depends on iterations)
- **Saliency/Simple**: ~0.1-0.3 seconds per image (fastest)

## Next Steps

1. **Test with Your Images**: Try different methods on your sample images
2. **Tune Parameters**: Adjust `cell_size`, `max_radius` for desired effect
3. **Integrate**: Add to main CLI with `--selective` flag
4. **Optimize**: Cache REMBG models, batch process for speed

## References

- **REMBG**: https://github.com/danielgatis/rembg
- **MediaPipe**: https://google.github.io/mediapipe/
- **U2Net**: https://github.com/xuebinqin/U-2-Net
- **GrabCut Algorithm**: OpenCV documentation

