# -*- coding:UTF-8 -*-

# [Usage]: python ./hanfeng.py '/home/haoming/WORK/scripts/hanfeng/NASJson/data_2164_None_vNone/2164.json','/media/haoming/Nothing/2164/2164/','/home/haoming/WORK/scripts/hanfeng/NASJson/data_2164_None_vNone/',

import os
import sys
import cv2
import logging
import json
import math

logging.basicConfig(level=logging.DEBUG)
[_scriptDir_, _scriptName_] = os.path.dirname(os.path.abspath(__file__)), os.path.basename(os.path.abspath(__file__))


class EyesParse():
    def __init__(self, jsonPath, imgPath, savePath):
        self.jsonPath = jsonPath
        self.imgPath = imgPath
        self.savePath = savePath
        self.jsonobj = []
        self.LoadJson(jsonPath)
        glass_path = savePath + os.sep + "glass" + os.sep
        #glass_close_path = savePath + os.sep + "glass_close" + os.sep
        normal_path = savePath + os.sep + "normal" + os.sep
        #a_close_path = savePath + os.sep + "a_close" + os.sep
        if not os.path.exists(glass_path):
            os.makedirs(glass_path)
        if not os.path.exists(normal_path):
            os.makedirs(normal_path)
        # if not os.path.exists(a_open_path):
        #     os.makedirs(a_open_path)
        # if not os.path.exists(a_close_path):
        #     os.makedirs(a_close_path)

    def Run(self):
        for ele in self.jsonobj:
            if self.isFrontFace(ele):
                try:
                   rightEyePos, leftEyePos, image_key = self.GetPosFromJson(ele)
                  # print      rightEyePos, leftEyePos, image_key
                   hasGlass= self.HasGlassAndOC(ele)
                   #print     hasGlass
                   [pos_x,pos_y,width,high]=self.ComparePos(rightEyePos,leftEyePos)
                   #print        pos_x,pos_y,width,high
                   self.DrawImg(image_key, pos_x,pos_y,width,high,hasGlass)
                except:
                  print 'wrong'
    def DrawImg(self, image_key, pos_x,pos_y,width,high,hasGlass):
        imagePath = os.path.join(self.imgPath, image_key)
        print  imagePath
        frame = cv2.imread(imagePath)
        if pos_y < 0 or pos_x < 0 or (pos_x + width) > 1280 or (pos_y + high) > 720:
            return
        print "1"
        print frame.shape[0]

        sub = frame[pos_y:pos_y + high, pos_x:pos_x + width]

        imgName = self.savePath

        if hasGlass:
            imgName = imgName + os.sep + "glass"
        else:
            imgName = imgName + os.sep + "normal"

        if len(sub) != 0 and len(sub[0]) != 0:
                tmp = imgName + os.sep + image_key
                print tmp
                cv2.imwrite(tmp,sub)

    def LoadJson(self, jsonPath):
        logging.debug("LoadJsong +")
        jsonlines = open(jsonPath, 'r').readlines()
        abandonJsonCount = 0
        for ele in jsonlines:
            if '#' in ele:
                abandonJsonCount = abandonJsonCount + 1
                continue
            self.jsonobj.append(json.loads(ele))
        logging.debug("Abandon %d lines from file", abandonJsonCount)
        logging.debug("Read %d lines from file", self.jsonobj.__len__())
        logging.debug("LoadJsong -")

    def GetPosFromJson(self, jsonrecorder):
        pos = jsonrecorder["face_keypoint_72"][0]["data"]
        image_key = jsonrecorder["image_key"]
        r_x0 = int(pos[13][0])
        r_y0 = int(pos[13][1])
        r_x1 = int(pos[21][0])
        r_y1 = int(pos[21][1])
        r_x2 = int(pos[17][0])
        r_y2 = int(pos[17][1])

        l_x0 = int(pos[30][0])
        l_y0 = int(pos[30][1])
        l_x1 = int(pos[38][0])
        l_y1 = int(pos[38][1])
        l_x2 = int(pos[34][0])
        l_y2 = int(pos[34][1])
        return [r_x0, r_y0, r_x1, r_y1, r_x2, r_y2], [l_x0, l_y0, l_x1, l_y1, l_x2, l_y2], image_key  # 右眼，左眼（圖片自我方向）
       # return [r_x0, r_y0, r_x1, r_y1, r_x2, r_y2 , l_x0, l_y0, l_x1, l_y1, l_x2, l_y2], image_key

    def HasGlassAndOC(self, jsonrecorder):
        data = jsonrecorder["head"]
        glass = None
        left = None
        right = None
        data_head = None

        for ele in data:
            if ele["attrs"]["ignore"] == "no":
                data_head = ele
                break

        if data_head["attrs"]["has_glasses"] == "glasses":
            glass = True
        else:
            glass = False
        return glass
		# if data_head["attrs"]["left_eye"] == "open":
        #     left = True
        # else:
        #     left = False
        # if data_head["attrs"]["right_eye"] == "open":
        #     right = True
        # else:
        #     right = False

        #, right, left

    def CalPos(self, Pos, x_scal=0.5, y_scal=1, w_scal=2.0, h_scal=2.0):
        p2x = Pos[4]
        p1x = Pos[0]
        p1y = Pos[1]
        pcx = Pos[2]
        pcy = Pos[3]
        width = p2x - p1x
        pos_x = p1x - x_scal * width
        pos_y = p1y - y_scal * width
        pos_w = width * w_scal
        pos_h = width * h_scal
        return int(pos_x), int(pos_y), int(pos_w), int(pos_h)

    def ComparePos(self,rightEyePos,leftEyePos):
        r_posx,r_posy,r_posw,r_posh=self.CalPos(rightEyePos)
        l_posx,l_posy,l_posw,l_posh=self.CalPos(leftEyePos)
        width=l_posx-r_posx+l_posw
        high=max(l_posh,r_posh)
        if r_posy>leftEyePos[5]:
			r_posy=leftEyePos[5]
			print '11111111111111111111111111111111111111111111111'
        return int(r_posx),int(r_posy),int(width),int(high)

    def isFrontFace(self, jsonrecorder):
        points = jsonrecorder["face_keypoint_72"][0]["data"]
        attrs = jsonrecorder["face_keypoint_72"][0]["point_attrs"]
        for i in range(13, 21):
            if attrs[i] != '':
                return False
        for i in range(30, 38):
            if attrs[i] != '':
                return False

        max_l = points[13][0]
        max_r = points[34][0]
        max_c = (max_l + max_r) / 2
        p_nose = points[57][0]

        tilt_rate = (p_nose - max_c) / (max_r - max_l)
        # print "tilt_rate", tilt_rate
        if math.fabs(tilt_rate) < 0.2:
            return True
        else:
            return False

def WalkDir(srcdir):
    list_dir = os.listdir(srcdir)#枚举出当前目录下的所有单位（包括目录和文件），具有不穿透目录的特性
    list_dstdir = []# 定义空白列表用以承载
    name_list=[]
    for ele in list_dir:
        name= os.path.join(ele)
        name_list.append(name)
    return name_list

if __name__ == '__main__':
	#in_put=raw_input()
	src_js='D:\Share\data\json'
	src_imgPath='D:\Share\data\image'
	out_Path='D:\Share\data\output_glass'
	for root,dirs,files in os.walk(src_js):
		for ele in files:
			if  ele.find('fix_fix')!=-1:
				key_id=root.split(os.sep)[-1]
				#key_id='1047'
				jspath=root+os.sep+ele
				imagePath=src_imgPath+os.sep+key_id
				out_imagePath=out_Path+os.sep+key_id
				if not os.path.exists(out_imagePath):
					os.makedirs(out_imagePath)
				print jspath,key_id,imagePath
				obj = EyesParse(
		           jspath,
		           imagePath,
		           out_imagePath )
				obj.Run()



















