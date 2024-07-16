"""Main module."""
import logging
import os
import json
import shutil
from zipfile import ZipFile

from fw_core_client import CoreClient
from flywheel_gear_toolkit import GearToolkitContext
import flywheel

from .get_tissue_mask import generate_tissue_mask
from .get_image_patches import generate_wsi_tiles

from .run_level import get_analysis_run_level_and_hierarchy
# from .get_analysis import get_matching_analysis

log = logging.getLogger(__name__)

fw_context = flywheel.GearContext()
fw = fw_context.client

def run(client: CoreClient, gtk_context: GearToolkitContext):
    """Main entrypoint

    Args:
        client (CoreClient): Client to connect to API
        gtk_context (GearToolkitContext)
    """
    # get the Flywheel hierarchy for the run
    destination_id = gtk_context.destination["id"]
    hierarchy = get_analysis_run_level_and_hierarchy(gtk_context.client, destination_id)
    acq_label = hierarchy['acquisition_label']
    sub_label = hierarchy['subject_label']
    ses_label = hierarchy['session_label']
    project_label = hierarchy['project_label']
    group_name = hierarchy['group']

    # get the output acqusition container
    acq = fw.lookup(f'{group_name}/{project_label}/{sub_label}/{ses_label}/{acq_label}')
    acq = acq.reload()

    # get the input file
    CONFIG_FILE_PATH = '/flywheel/v0/config.json'
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)

    input_file_name = config['inputs']['input_image']['location']['path']
    threshold_flag = config['config']['threshold_tiles']
    low_contrast_flag = config['config']['exclude_low_contrast_tiles']

    # run the main processes & upload output file back to acquisition
    print(f'Generating tiles for file: {input_file_name}')
    output_dir = input_file_name.replace('.svs','_tiles') # assumes this is an SVS file type
    output_dir = output_dir.replace(' ','_')
    generate_wsi_tiles(input_file_name, output_dir, threshold_flag, low_contrast_flag)

    print(f'Zipping the output folder: {output_dir}')
    with ZipFile(f'{output_dir}.zip', 'w') as zip_object:
        # Traverse all files in directory
        for folder_name, sub_folders, file_names in os.walk(f'{output_dir}'):
            for filename in file_names:
                # Create filepath of files in directory
                file_path = os.path.join(folder_name, filename)
                # Add files to zip file
                zip_object.write(file_path, os.path.basename(file_path))

    print(f'Uploading tiles to acquisition: {acq.label}/{output_dir}.zip')
    acq.upload_file(f'{output_dir}.zip')
    os.remove(f'{output_dir}.zip') # remove from instance to save space
