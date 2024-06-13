# based on: https://digitalslidearchive.github.io/HistomicsTK/examples/nuclei_segmentation.html

import os

import histomicstk as htk

import skimage.io
import skimage.measure
import skimage.color
import large_image

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#Some nice default configuration for plots
plt.rcParams['figure.figsize'] = 10, 10
plt.rcParams['image.cmap'] = 'gray'
titlesize = 24

# load image
# inputImageFile = 'C1155462_7316-4187_H_and_E.svs'

def generate_wsi_tiles(inputImageFile, output_dir):

    # imInput = skimage.io.imread(inputImageFile)[:, :, :3]

    # # binarize the mask
    # tissue_mask = np.where(tissue_mask > 0, 1, 0)

    # # mask the image to only select tissue regions
    # imInput[:,:,0] = tissue_mask * imInput[:,:,0]
    # imInput[:,:,1] = tissue_mask * imInput[:,:,1]
    # imInput[:,:,2] = tissue_mask * imInput[:,:,2]
    # skimage.io.imsave(f"masked_image.tiff", imInput)

    # ============ get image tiles ============================================
    ts = large_image.getTileSource(inputImageFile)

    # ============ run main steps on each tile ============================================
    for tile_info in ts.tileIterator(
                            region=dict(left=5000, top=5000, width=20000, height=20000, units='base_pixels'),
                            scale=dict(magnification=20),
                            tile_size=dict(width=1000, height=1000),
                            tile_overlap=dict(x=50, y=50),
                            format=large_image.tilesource.TILE_FORMAT_PIL,
                        ):
        # print(tile_info)
        tile_num = tile_info['tile_position']['position']
        print(f'PROCESSING TILE # {tile_num}')

        tile_im = ts.getSingleTile(
                        tile_size=dict(width=tile_info['width'], height=tile_info['height']),
                        scale=dict(magnification=tile_info['magnification']),
                        tile_position=tile_info['tile_position'],
                    )
        this_tile_image = tile_im['tile']

        # save tile
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        skimage.io.imsave(f"{output_dir}/{tile_num}.png", this_tile_image)




    # # get a single tile
    # pos = 1500
    # tile_info = ts.getSingleTile(
    #     tile_size=dict(width=500, height=500),
    #     scale=dict(magnification=20),
    #     tile_position=pos,
    # )
    # plt.imshow(tile_info['tile'])
    # plt.show()
    # plt.hist(tile_info['tile'][:,:,1])
    # plt.show()
