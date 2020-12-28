import pickle
import shutil 
from tqdm import tqdm as tqdm
import os
import pickle

"""
    This file creates a combined dataset of train and extra folder images
    Joins and creates a new annotation file using the already processed train and extra annotations
    The combined dataset annotation file has the format specified below

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
print('---------------- combining processed train and extra annotation files to combined annotation file ----------------')

with open('./train_annotations_processed.pkl' , 'rb') as f:
    train_annotations = pickle.load(f)
with open('./extra_annotations_processed.pkl' , 'rb') as f:
    extra_annotations = pickle.load(f)

if not os.path.exists("./combined/"):
    os.makedirs('./combined/')

print(len(train_annotations),len(extra_annotations))

final_annotations = train_annotations.copy()

for i in tqdm(train_annotations.keys()):
    train_src_path =  "./train/" + i
    train_target_path =  "./combined/" + i
    shutil.copyfile(train_src_path,train_target_path)

for i in tqdm(extra_annotations.keys()):
    new_img_index = len(train_annotations) + int(i.split('.')[0])
    new_img_abs_path = str(new_img_index) + '.' + i.split('.')[1]
    final_annotations[new_img_abs_path] = extra_annotations[i]
    extra_src_path =  "./extra/" + i
    extra_target_path =  "./combined/" + new_img_abs_path
    shutil.copyfile(extra_src_path,extra_target_path)


with open('./combined_annotations_processed.pkl' , 'wb') as f:
    pickle.dump(final_annotations,f)

print('---------------- processing completed ----------------')