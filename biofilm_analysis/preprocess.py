import numpy as np
from scipy.ndimage import gaussian_filter

def normalize_local_contrast(img, block_diameter):
    img = 1.0 - img
    blurred = gaussian_filter(img.copy(), sigma=block_diameter / 6)
    return img - blurred

def preprocess_stack(stack, block_diameter, sigma):
    return np.stack([
        gaussian_filter(normalize_local_contrast(stack[..., t], block_diameter), sigma=sigma)
        for t in range(stack.shape[2])
    ], axis=2)

