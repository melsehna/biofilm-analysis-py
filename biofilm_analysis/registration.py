import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift, fftfreq

def phase_offset(source, target, upsample_factor=1, normalize=False):
    source_freq = fft2(source)
    target_freq = fft2(target)
    image_product = source_freq * np.conj(target_freq)

    if normalize:
        image_product /= np.maximum(np.abs(image_product), np.finfo(np.float64).eps)

    if upsample_factor == 1:
        cross_correlation = ifft2(image_product)
    else:
        cross_correlation = ifft2(image_product)

    maxima = np.max(np.abs(cross_correlation))
    maxidx = np.unravel_index(np.argmax(np.abs(cross_correlation)), cross_correlation.shape)
    shape = source_freq.shape
    midpoints = [dim // 2 for dim in shape]

    shift = []
    for i, mi, s in zip(maxidx, midpoints, shape):
        if i > mi:
            shift.append(i - s)
        else:
            shift.append(i)

    shift = np.array(shift, dtype=np.float64)

    if upsample_factor == 1:
        error, phasediff = calculate_stats(maxima, source_freq, target_freq)
        return shift, error, phasediff

    # refine shift with upsampling
    shift = np.round(shift * upsample_factor) / upsample_factor
    upsample_region_size = int(np.ceil(upsample_factor * 1.5))
    dftshift = upsample_region_size // 2
    sample_region_offset = dftshift - shift * upsample_factor

    cross_correlation = upsampled_dft(
        image_product,
        upsample_region_size,
        upsample_factor,
        sample_region_offset
    )

    maxima = np.max(np.abs(cross_correlation))
    maxidx = np.unravel_index(np.argmax(np.abs(cross_correlation)), cross_correlation.shape)
    shift += (np.array(maxidx) - dftshift) / upsample_factor

    error, phasediff = calculate_stats(maxima, source_freq, target_freq)
    return shift, error, phasediff


def upsampled_dft(data, region_size, upsample_factor, offsets):
    """
    Emulates Julia's upsampled DFT from a small region around the peak.
    """
    nr, nc = data.shape
    sample_rate = 1.0 / upsample_factor
    shiftrange = np.arange(region_size)

    # frequency vectors
    rfreqs = fftfreq(nr, d=sample_rate)
    cfreqs = fftfreq(nc, d=sample_rate)

    # kernel in col direction
    kernel_c = np.exp(
        -2j * np.pi * (shiftrange[:, None] - offsets[0]) * cfreqs[None, :]
    )
    # kernel in row direction
    kernel_r = np.exp(
        2j * np.pi * (shiftrange[:, None] - offsets[1]) * rfreqs[None, :]
    )

    result = kernel_r @ (data * kernel_c).T
    return result


def calculate_stats(crosscor_maxima, source_freq, target_freq):
    source_amp = np.mean(np.abs(source_freq) ** 2)
    target_amp = np.mean(np.abs(target_freq) ** 2)
    error = 1 - (np.abs(crosscor_maxima) ** 2) / (source_amp * target_amp)
    phasediff = np.angle(crosscor_maxima)
    return error, phasediff

from scipy.ndimage import shift as apply_shift

def register_and_crop(stack, shifts_array, crop_indices):
    """Register each frame of the input stack using given shifts and crop."""
    registered = np.empty_like(stack)
    registered[..., 0] = stack[..., 0]
    for t in range(1, stack.shape[2]):
        registered[..., t] = apply_shift(stack[..., t], shifts_array[t - 1], order=3, mode='reflect')

    row_min, row_max, col_min, col_max = crop_indices
    cropped = registered[row_min:row_max, col_min:col_max, :]
    return cropped

