# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:59:59 2017

@author: root
"""

import os
import cv2
import json



ori_json_path = '/mnt/hgfs/Share/data_000001.json'
lines = open(ori_json_path, 'r').readlines()
ori_json_format = json.loads(lines[2])
#ori_json_format.pop('face_keypoint_29')

img_path = '/mnt/hgfs/seagate/umdface/'
txt_path = '/mnt/hgfs/seagate/umdface/det_umd3_align.txt'
lines = open(txt_path,'r').readlines()

new_jsonfile=open('/mnt/hgfs/seagate/umdface/umd3_det_new.json','wb')

i = 0
while i <len(lines):
    new_json = ori_json_format
    img_name = lines[i].strip('\n').split('/')[1]
    img = cv2.imread(img_path+lines[i].strip('\n'))
    new_json['image_key'] = img_name
    new_json['height'] = int(img.shape[0])
    new_json['width'] = int(img.shape[1])
    new_json['video_index'] = str(i/2+1)
    
    rects = lines[i+1].split(' ')
    head = []     
    for k in range(0,len(rects)-1,4):
        obj = dict()
        obj['data'] = [float(rects[k]),float(rects[k+1]),float(rects[k+2]),float(rects[k+3])]
        obj['id'] = (k/4)+1
        obj["struct_type"] = "rect"
        obj['track_id'] = -1
        obj['attrs'] = dict()
        obj['attrs']['has_glasses'] = 'glasses'
        obj['attrs']['ignore'] = 'no'
        obj['attrs']['left_eye'] = 'open'
        obj['attrs']['right_eye'] = 'open'
        obj['attrs']['smoke'] = 'no'
        head.append(obj)
    new_json['head'] = head
    new_jsonfile.write(json.dumps(new_json)+'\n')
    i=i+2

new_jsonfile.close()
