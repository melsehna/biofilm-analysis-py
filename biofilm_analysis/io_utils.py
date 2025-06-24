import tifffile
import pandas as pd
import numpy as np

def load_tif_stack(path):
    stack = tifffile.imread(path)
    if stack.shape[0] < stack.shape[-1]:
        stack = np.transpose(stack, (1, 2, 0))
    return stack

def save_stack(path, stack):
    tifffile.imwrite(path, stack.astype(np.float32))

import tifffile
import numpy as np

import numpy as np
import tifffile
from skimage.color import gray2rgb
from skimage.util import img_as_ubyte

def save_overlay_stack(path, grayscale_stack, mask_stack):
    """Saves RGB stack with cyan overlay on masked regions."""
    grayscale_stack = np.clip(grayscale_stack, 0, 1)
    rgb_stack = np.repeat(grayscale_stack[..., np.newaxis], 3, axis=-1)
    overlay = rgb_stack.copy()
    overlay[mask_stack.astype(bool)] = [0, 1, 1]  # cyan
    tifffile.imwrite(path, (overlay * 255).astype(np.uint8), imagej=True)

def save_grayscale_stack(path, stack):
    stack = np.clip(stack, 0, 1)
    tifffile.imwrite(path, (stack * 255).astype(np.uint8), imagej=True)

def compute_OD_stack(images, Imin, Imax=None):
    eps = np.finfo(np.float32).eps
    if Imax is not None:
        return -np.log10((images - Imin + eps) / (Imax - Imin + eps))
    else:
        return -np.log10((images - Imin + eps) / (images[..., 0] - Imin + eps))

def save_OD_stack(path_prefix, OD_stack):
    """Save OD-transformed stack as individual grayscale .tif slices."""
    for t in range(OD_stack.shape[2]):
        path = f'{path_prefix}_OD_t{t+1}.tif'
        tifffile.imwrite(path, (OD_stack[..., t] * 255).astype(np.uint8), imagej=True)

def save_biomass_csv(path, biomass, name='Well1'):
    df = pd.DataFrame({name: biomass})
    df.to_csv(path, index=False)
    
def find_matching_channels(target_path, all_paths):
    target_base = Path(target_path).stem
    base_parts = target_base.split('_')
    well_id = '_'.join(base_parts[:2])
    return [
        p for p in all_paths
        if well_id in Path(p).stem and 'BF' not in Path(p).stem and p != target_path
    ]


