import numpy as np

def compute_mask(stack, threshold):
    return stack > threshold

def dust_correct(mask):
    first = mask[..., 0]
    for t in range(1, mask.shape[2]):
        mask[..., t][first & ~mask[..., t]] = False
    return mask

