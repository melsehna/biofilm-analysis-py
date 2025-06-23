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

def save_overlay_stack(path, original_stack, mask_stack):
    from skimage.color import gray2rgb

    overlay = np.zeros(original_stack.shape + (3,), dtype=np.uint8)
    for t in range(original_stack.shape[2]):
        base = gray2rgb((original_stack[..., t] * 255).astype(np.uint8))
        base[mask_stack[..., t]] = [0, 255, 255]  # cyan for mask
        overlay[..., t, :] = base
    # save as multi-page tif
    tifffile.imwrite(path, overlay.transpose(2, 0, 1, 3))  # (T, Y, X, 3)

def save_grayscale_stack(path, stack):
    tifffile.imwrite(path, (stack.transpose(2, 0, 1) * 255).astype(np.uint8))

def save_biomass_csv(path, biomass, name='Well1'):
    df = pd.DataFrame({name: biomass})
    df.to_csv(path, index=False)

