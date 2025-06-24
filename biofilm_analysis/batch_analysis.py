import pandas as pd
import re
from pathlib import Path


# python batch_analysis.py --config experiment_config.json


def load_protocol(image_dir):
    proto_path = Path(image_dir) / 'protocol.csv'
    if not proto_path.exists():
        raise FileNotFoundError(f'Protocol file not found at {proto_path}')
    df = pd.read_csv(proto_path)
    return df[df['action'] == 'Imaging Read']


def group_files(image_dir, protocol_df):
    tif_files = list(Path(image_dir).glob('*.tif'))
    grouped = {}

    for _, row in protocol_df.iterrows():
        step = row['step']
        mag = row['magnification']
        channel = row['channel']
        pattern = f'_0{step}_'
        matching_files = [f for f in tif_files if pattern in f.name and channel in f.name]
        key = (mag, channel)
        grouped.setdefault(key, []).extend(matching_files)

    return grouped


def group_by_well(file_list):
    wells = {}
    for f in file_list:
        well_match = re.match(r'([A-H]\d+)', f.name)
        if well_match:
            well = well_match.group(1)
            wells.setdefault(well, []).append(f)
    return wells

def full_plate_analysis(image_dir, config):
    protocol_df = load_protocol(image_dir)
    grouped = group_files(image_dir, protocol_df)

    for (mag, channel), files in grouped.items():
        wells = group_by_well(files)
        for well, well_files in wells.items():
            if channel == 'Bright Field':
                # Run BF pipeline (gives mask, shifts)
                result = process_brightfield_stack(well_files, config, image_dir, well, mag)
            else:
                # Apply BF-derived transforms
                process_channel_stack(well_files, result, image_dir, well, mag, channel)

df = pd.DataFrame(biomass_matrix, columns=well_names)
df.to_csv(output_dir / f'{mag}_{channel}_biomass.csv', index=False)

