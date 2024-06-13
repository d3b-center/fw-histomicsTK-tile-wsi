import skimage.io
from histomicstk.saliency.tissue_detection import (
    get_slide_thumbnail, get_tissue_mask)

def generate_tissue_mask(inputImageFile):
    imInput = skimage.io.imread(inputImageFile)[:, :, :3]

    mask_out, _ = get_tissue_mask(
        imInput, deconvolve_first=True,
        n_thresholding_steps=1, sigma=1.5, min_size=30)

    skimage.io.imsave(f"tissue_mask.png", mask_out)

