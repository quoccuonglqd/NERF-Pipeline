import shutil
import random
import numpy as np
import matplotlib.pyplot as plt
import os.path as osp
from os import listdir
import cv2 as cv
from sklearn.model_selection import train_test_split
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--folder_dir', help = 'data path', default = './results')
args = parser.parse_args()

folder_dir = args.folder_dir

def cmp(x):
  return int(x[2:-4])
ls = [x for x in listdir(folder_dir) if x[-4:]=='.png']
ls.sort(key=cmp)
total_index = [str(x) for x in range(500)]
train_index, test_index = train_test_split(total_index, test_size=0.8, random_state=42)
val_index, test_index = train_test_split(test_index, test_size=0.5, random_state=42)
data = json.load(open(folder_dir + '/transforms.json'))
# for x in data:
#   print(x)
train_data = {'camera_angle_x': data['camera_angle_x']}
test_data = {'camera_angle_x': data['camera_angle_x']}
val_data = {'camera_angle_x': data['camera_angle_x']}
# for i in range(len(data['frames'])):
#   x = str(i)
#   if x != data['frames'][i]['file_path'][-len(x):]:
#     print(x)
train_frame = []
val_frame = []
test_frame = []
for i in range(len(data['frames'])):
  if str(i) in train_index:
    data['frames'][i]['file_path'] = './train/r_{}'.format(str(i))
    train_frame.append(data['frames'][i])
    shutil.move(osp.join(folder_dir, 'r_{}.png'.format(str(i))),\
                osp.join(folder_dir + '/{}/train'.format(model_name), 'r_{}.png'.format(str(i))))
  elif str(i) in test_index:
    data['frames'][i]['file_path'] = './test/r_{}'.format(str(i))
    test_frame.append(data['frames'][i])
    shutil.move(osp.join(folder_dir, 'r_{}.png'.format(str(i))),\
                osp.join(folder_dir + '/{}/test'.format(model_name), 'r_{}.png'.format(str(i))))
  else:
    data['frames'][i]['file_path'] = './val/r_{}'.format(str(i))
    val_frame.append(data['frames'][i])
    shutil.move(osp.join(folder_dir, 'r_{}.png'.format(str(i))),\
                osp.join(folder_dir + '/{}/val'.format(model_name), 'r_{}.png'.format(str(i))))
train_data['frames'] = train_frame
test_data['frames'] = test_frame
val_data['frames'] = val_frame
with open(folder_dir + '/transforms_train.json', 'w') as out_file:
  json.dump(train_data, out_file, indent=4)
with open(folder_dir + '/transforms_test.json', 'w') as out_file:
  json.dump(test_data, out_file, indent=4)
with open(folder_dir + '/transforms_val.json', 'w') as out_file:
  json.dump(val_data, out_file, indent=4)