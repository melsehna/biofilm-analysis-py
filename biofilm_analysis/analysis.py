from .preprocess import preprocess_stack
from .registration import phase_offset
from .segmentation import compute_mask, dust_correct
from .biomass import compute_biomass
from scipy.ndimage import shift as apply_shift

def compute_channel_biomass(stack, mask):
    nframes = stack.shape[2]
    biomass = np.zeros(nframes)
    for t in range(nframes):
        frame = stack[..., t]
        background = np.mean(frame[~mask[..., t]])
        biomass[t] = np.mean((frame - background) * mask[..., t])
    return biomass


def analyze_stack(stack, block_diameter, threshold, sigma=2, max_shift=50, upsample_factor=1, Imin=None, Imax=None, dust=True):

    norm = preprocess_stack(stack, block_diameter, sigma)
    
    # register stack
    shifts_array = []
    shifts = np.array([0.0, 0.0])

    for t in range(stack.shape[2]):
        norm_img = normalize_local_contrast(stack[..., t], block_diameter)
        blurred = gaussian_filter(norm_img, sigma=sigma)
        normalized[..., t] = blurred

        if t == 0:
            registered[..., t] = blurred
        else:
            fixed = normalized[..., t - 1]
            moving = blurred

            shift, _, _ = phase_offset(fixed, moving, upsample_factor=upsample_factor, normalize=True)
            shift_norm = np.linalg.norm(shift)

            if shift_norm >= max_shift:
                # Too large → use previous shift
                shift_to_apply = shifts
            else:
                shift = -shift
                shift_to_apply = shift + shifts
                shifts = shift_to_apply

            shifts_array.append(shift_to_apply)
            registered[..., t] = apply_shift(moving, shift_to_apply, order=3, mode='reflect')
            stack[..., t] = apply_shift(stack[..., t], shift_to_apply, order=3, mode='reflect')

    mask = compute_mask(reg, threshold)
    if dust:
        mask = dust_correct(mask)
        
    biomass = np.zeros(stack.shape[2])
    OD_stack = None

    if Imin is not None:
        OD_stack = compute_OD_stack(stack, Imin, Imax)
        for t in range(stack.shape[2]):
            masked = OD_stack[..., t] * mask[..., t]
            biomass[t] = masked.mean()
    else:
        for t in range(stack.shape[2]):
            masked = (1.0 - stack[..., t]) * mask[..., t]
            biomass[t] = masked.mean()

    return {
    'normalized': normalized,
    'registered': registered,
    'mask': mask,
    'biomass': biomass,
    'OD_stack': OD_stack
}


