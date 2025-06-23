import numpy as np

def compute_biomass(stack, mask, Imin=None, Imax=None):
    biomass = []
    for t in range(stack.shape[2]):
        img = stack[..., t]
        msk = mask[..., t]
        if Imin is not None and Imax is not None:
            od = -np.log10((img - Imin) / (Imax - Imin))
            biomass.append(np.mean(od[msk]))
        else:
            biomass.append(np.mean((1.0 - img)[msk]))
    return biomass

