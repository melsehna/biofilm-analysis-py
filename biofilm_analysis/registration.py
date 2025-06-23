from scipy.ndimage import fourier_shift
from skimage.registration import phase_cross_correlation
import numpy as np

def register_stack(stack, max_shift=50):
    shifts = []
    registered = np.zeros_like(stack)
    registered[..., 0] = stack[..., 0]
    cum_shift = np.array([0.0, 0.0])
    for t in range(1, stack.shape[2]):
        shift, _, _ = phase_cross_correlation(stack[..., t-1], stack[..., t])
        if np.linalg.norm(shift) >= max_shift:
            shift = cum_shift
        else:
            cum_shift += -shift
        shifts.append(cum_shift.copy())
        reg = np.fft.ifftn(fourier_shift(np.fft.fftn(stack[..., t]), cum_shift)).real
        registered[..., t] = reg
    return registered, shifts

