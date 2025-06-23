import argparse
import os
from pathlib import Path
from glob import glob

from biofilm_analysis.io_utils import (
    load_tif_stack, save_biomass_csv, save_overlay_stack, save_grayscale_stack
)
from biofilm_analysis.config import load_config
from biofilm_analysis.analysis import analyze_stack


def process_single_file(stack_path, outdir, config):
    print(f'Processing: {stack_path}')
    filename = Path(stack_path).stem


	block = args.block if args.block else int(config['blockDiam'])
	thresh = args.thresh if args.thresh else float(config['fixed_thresh'])
	sigma = args.sigma if args.sigma else 2
	max_shift = args.maxshift if args.maxshift else 50
	dust = not args.nodust if 'dust_correction' in config else True

	result = analyze_stack(
	    stack,
	    block_diameter=block,
	    threshold=thresh,
	    sigma=sigma,
	    max_shift=max_shift,
	    Imin=None,
	    Imax=None,
	    dust=dust
	)

    os.makedirs(outdir, exist_ok=True)
    save_biomass_csv(f"{outdir}/biomass_{filename}.csv", result['biomass'])

    # Save overlays
    save_overlay_stack(f"{outdir}/{filename}_mask_overlay.tif", stack, result['mask'])
    save_grayscale_stack(f"{outdir}/{filename}_registered.tif", result['registered'])

def main():
	parser = argparse.ArgumentParser(description='Biofilm analysis pipeline.')
	parser.add_argument('--file', type=str, help='Path to a single .tif file')
	parser.add_argument('--batch', action='store_true', help='Process all .tif files in config directory')
	parser.add_argument('--outdir', type=str, default='output/', help='Where to save outputs')
	parser.add_argument('--block', type=int, help='Block diameter for contrast normalization')
	parser.add_argument('--thresh', type=float, help='Threshold for masking')
	parser.add_argument('--sigma', type=float, help='Gaussian blur sigma')
	parser.add_argument('--maxshift', type=float, help='Max registration shift')
	parser.add_argument('--nodust', action='store_true', help='Disable dust correction')

    args = parser.parse_args()

    config = load_config()
    image_dir = config['images_directory'][0]

    if args.batch:
        tiff_paths = sorted(glob(f'{image_dir}/*.tif'))
        for tif_path in tiff_paths:
            process_single_file(tif_path, args.outdir, config)
    elif args.file:
        process_single_file(args.file, args.outdir, config)
    else:
        print("Please provide either --file or --batch")




if __name__ == '__main__':
    main()

