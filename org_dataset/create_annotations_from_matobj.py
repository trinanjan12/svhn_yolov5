
"""
    This file extracts data from svhn dataset .mat file
    creates annotation files in the format shown below

{'1.png': {'height': [219, 219],
  'left': [246, 323],
  'top': [77, 81],
  'width': [81, 96],
  'label': [1, 9]},
 '2.png': {'height': [32, 32],
  'left': [77, 98],
  'top': [29, 25],
  'width': [23, 26],
  'label': [2, 3]} }
}

"""

from glob import glob as glob
import h5py
import numpy as np
import os
from tqdm import tqdm as tqdm
import pickle
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--mode", default = "test",  type=str , help="mode of folder train/test/extra")
args = parser.parse_args()

# Helper functions
# to decode the mat annotation file
bbox_prop = ['height', 'left', 'top', 'width', 'label']


def get_img_boxes(f, idx=0):
    """
    get the 'height', 'left', 'top', 'width', 'label' of bounding boxes of an image
    :param f: h5py.File
    :param idx: index of the image
    :return: dictionary
    """
    meta = {key: [] for key in bbox_prop}

    box = f[bboxs[idx][0]]
    for key in box.keys():
        if box[key].shape[0] == 1:
            meta[key].append(int(box[key][0][0]))
        else:
            for i in range(box[key].shape[0]):
                meta[key].append(int(f[box[key][i][0]][()].item()))

    return meta


def get_img_name(f, idx=0):
    img_name = ''.join(map(chr, f[names[idx][0]][()].flatten()))
    return(img_name)


# Global Settings
mode = args.mode
anno_filename = os.path.join(mode, 'digitStruct.mat')
anno_file_data = h5py.File(anno_filename, 'r')
names = anno_file_data['digitStruct/name']
bboxs = anno_file_data['digitStruct/bbox']

total_num_file = anno_file_data['digitStruct/name'].shape[0]
print(f'Loading and processing --> {anno_filename}')
print(f'Total number of image to process are --> {total_num_file}')
print('---------------- Processing and creating annotation file from the .mat format file ----------------')
annotations = {}

# Processing code
for index in tqdm(range(total_num_file)):
    img_name, img_bbox = get_img_name(
        anno_file_data, index), get_img_boxes(anno_file_data, index)
    # the svhn dataset assigns the class label "10" to the digit 0
    # this makes it inconsistent with several loss functions
    # which expect the class labels to be in the range [0, C-1]
    for i, v in enumerate(img_bbox['label']):
        if v == 10:
            img_bbox['label'][i] = 0
    annotations[img_name] = img_bbox
print('saving processed annotations')
filename = mode + '_annotations_processed.pkl'
with open(filename, 'wb') as f:
    pickle.dump(annotations, f)
print('---------------- Processign Done ----------------')
