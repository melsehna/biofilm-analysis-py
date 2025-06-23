from .preprocess import preprocess_stack
from .registration import register_stack
from .segmentation import compute_mask, dust_correct
from .biomass import compute_biomass

def analyze_stack(stack, block_diameter, threshold, sigma,
                  Imin=None, Imax=None, dust=True, max_shift=50):
    norm = preprocess_stack(stack, block_diameter, sigma)
    reg, shifts = register_stack(norm, max_shift)
    mask = compute_mask(reg, threshold)
    if dust:
        mask = dust_correct(mask)
    biomass = compute_biomass(stack, mask, Imin, Imax)
    return {
        'registered': reg,
        'mask': mask,
        'biomass': biomass,
        'shifts': shifts
    }

