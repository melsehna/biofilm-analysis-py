import numpy as np
from scipy.ndimage import uniform_filter

def compute_integral_image(img):
    return img.cumsum(axis=0).cumsum(axis=1)

def mean_filter_integral(img, length_scale):
    """Perform mean filtering using integral image over square window."""
    h, w = img.shape
    d = length_scale

    integral = compute_integral_image(img)

    padded = np.pad(integral, ((1, 0), (1, 0)), mode='constant', constant_values=0)

    x1 = np.clip(np.arange(h) - d, 0, h - 1)
    x2 = np.clip(np.arange(h) + d + 1, 0, h)
    y1 = np.clip(np.arange(w) - d, 0, w - 1)
    y2 = np.clip(np.arange(w) + d + 1, 0, w)

    mean = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            a = padded[x1[i], y1[j]]
            b = padded[x1[i], y2[j]]
            c = padded[x2[i], y1[j]]
            d_ = padded[x2[i], y2[j]]
            area = (x2[i] - x1[i]) * (y2[j] - y1[j])
            mean[i, j] = (d_ - b - c + a) / max(area, 1)

    return mean

def normalize_local_contrast(img, block_diameter):
    """Invert + subtract mean-filtered version, rescale to [0, 1]"""
    fp_max = np.max(img)
    fp_min = np.min(img)
    fp_mean = (fp_max - fp_min) / 2.0 + fp_min
    length_scale = (block_diameter - 1) // 2

    baseline = mean_filter_integral(img, length_scale)
    normalized = img - baseline + fp_mean
    normalized = np.clip(normalized, 0, 1)
    return normalized


def preprocess_stack(stack, block_diameter, sigma):
    return np.stack([
        gaussian_filter(normalize_local_contrast(stack[..., t], block_diameter), sigma=sigma)
        for t in range(stack.shape[2])
    ], axis=2)

