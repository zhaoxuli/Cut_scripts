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
        glass_open_path = savePath + os.sep + "glass_open" + os.sep
        glass_close_path = savePath + os.sep + "glass_close" + os.sep
        a_open_path = savePath + os.sep + "a_open" + os.sep
        a_close_path = savePath + os.sep + "a_close" + os.sep
        if not os.path.exists(glass_open_path):
            os.makedirs(glass_open_path)
        if not os.path.exists(glass_close_path):
            os.makedirs(glass_close_path)
        if not os.path.exists(a_open_path):
            os.makedirs(a_open_path)
        if not os.path.exists(a_close_path):
            os.makedirs(a_close_path)

    def Run_29(self):
        for ele in self.jsonobj:
             try :
                if self.isFrontFace_29(ele):
                    try:
                        rightEyePos, leftEyePos, image_key = self.GetPosFromJson_29(ele)
                        hasGlass, rightState, leftState = self.HasGlassAndOC(ele)
                        [rpos_x, rpos_y, rpos_w, rpos_h] = self.CalPos(rightEyePos)
                        [lpos_x, lpos_y, lpos_w, lpos_h] = self.CalPos(leftEyePos)
                        self.DrawImg(image_key, rpos_x, rpos_y, rpos_w, rpos_h, lpos_x, lpos_y, lpos_w, lpos_h, hasGlass,
                                     rightState, leftState)
                    except:
                        print "eye  location wrong"
                else:
                    print 'false'
             except:
               print  ele['image_key'],'  dont have lmk'

    def Run_72(self):
        for ele in self.jsonobj:
             try :
                if self.isFrontFace_72(ele):
                    try:
                        rightEyePos, leftEyePos, image_key = self.GetPosFromJson_72(ele)
                        hasGlass, rightState, leftState = self.HasGlassAndOC(ele)
                        [rpos_x, rpos_y, rpos_w, rpos_h] = self.CalPos(rightEyePos)
                        [lpos_x, lpos_y, lpos_w, lpos_h] = self.CalPos(leftEyePos)
                        self.DrawImg(image_key, rpos_x, rpos_y, rpos_w, rpos_h, lpos_x, lpos_y, lpos_w, lpos_h, hasGlass,
                                     rightState, leftState)
                    except:
                        print "eye  location wrong"
                else:
                    print 'false'
             except:
               print  ele['image_key'],'  dont have lmk'

    def DrawImg(self, image_key, rpos_x, rpos_y, rpos_w, rpos_h, lpos_x, lpos_y, lpos_w, lpos_h, hasGlass, rightState,leftState):
        imagePath = os.path.join(self.imgPath, image_key)
        frame = cv2.imread(imagePath)
        if lpos_y < 0 or lpos_x < 0 or (lpos_x + lpos_w) > 1280 or (lpos_y + lpos_h) > 720:
            return
        l_sub = frame[lpos_y:lpos_y + lpos_h, lpos_x:lpos_x + lpos_w]
        r_sub = frame[rpos_y:rpos_y + rpos_h, rpos_x:rpos_x + rpos_w]
        imgName = self.savePath

        if hasGlass:
            imgName = imgName + os.sep + "glass_"
        else:
            imgName = imgName + os.sep + "a_"

        if len(l_sub) != 0 and len(l_sub[0]) != 0:
            if leftState == 0:
                tmp = imgName + "open" + os.sep + 'left_' + image_key
                cv2.imwrite(tmp, l_sub)
            elif leftState == 1:
                tmp = imgName + "close" + os.sep + 'left_' + image_key
                cv2.imwrite(tmp, l_sub)

        if len(r_sub) != 0 and len(r_sub[0]) != 0:
            if rightState == 0:
                tmp = imgName + "open" + os.sep + 'right_' + image_key
                cv2.imwrite(tmp, r_sub)
            elif rightState ==1:
                tmp = imgName + "close" + os.sep + 'right_' + image_key
                cv2.imwrite(tmp, r_sub)
        print imagePath

    def LoadJson(self, jsonPath):
        logging.debug("LoadJsong +")
        jsonlines = open(jsonPath, 'r').readlines()
        abandonJsonCount = 0
        for ele in jsonlines:
            if '#' in ele:
                abandonJsonCount = abandonJsonCount + 1
                continue
            self.jsonobj.append(json.loads(ele))
      #  logging.debug("Abandon %d lines from file", abandonJsonCount)
      #  logging.debug("Read %d lines from file", self.jsonobj.__len__())
      #  logging.debug("LoadJsong -")

    def GetPosFromJson_29(self, jsonrecorder):
        pos = jsonrecorder["face_keypoint_29"][0]["data"]
        image_key = jsonrecorder["image_key"]
        r_x0 = int(pos[6][0])
        r_y0 = int(pos[6][1])
        r_x1 = int(pos[10][0])
        r_y1 = int(pos[10][1])
        r_x2 = int(pos[8][0])
        r_y2 = int(pos[8][1])

        l_x0 = int(pos[11][0])
        l_y0 = int(pos[11][1])
        l_x1 = int(pos[15][0])
        l_y1 = int(pos[15][1])
        l_x2 = int(pos[13][0])
        l_y2 = int(pos[13][1])
        return [r_x0, r_y0, r_x1, r_y1, r_x2, r_y2], [l_x0, l_y0, l_x1, l_y1, l_x2, l_y2], image_key  # 右眼，左眼（圖片自我方向）

    def GetPosFromJson_72(self, jsonrecorder):
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
        print 'get-72 points'
        return [r_x0, r_y0, r_x1, r_y1, r_x2, r_y2], [l_x0, l_y0, l_x1, l_y1, l_x2, l_y2], image_key  # 右眼，左眼（圖片自我方向）

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

        if data_head["attrs"]["has_glasses"] == "none":
            glass = False
        else:
            glass = True
        if data_head["attrs"]["left_eye"] == "open":
            left = 0
        elif data_head["attrs"]["left_eye"] == "close":
            left = 1
        else:
            left = -1
        if data_head["attrs"]["right_eye"] == "open":
            right = 0
        elif data_head["attrs"]["right_eye"] == "close":
            right = 1
        else:
            right = -1

        return glass, right, left

    def CalPos(self, Pos, x_scal=0.5, y_scal=1.0, w_scal=2.0, h_scal=2.0):
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

    def isFrontFace_29(self, jsonrecorder):
        points = jsonrecorder["face_keypoint_29"][0]["data"]
        attrs = jsonrecorder["face_keypoint_29"][0]["point_attrs"]
        for i in range(6, 10):
            if attrs[i] != 'full_visible':
                return False
        for i in range(11, 15):
            if attrs[i] != 'full_visible':
                return False

        max_l = points[6][0]
        max_r = points[13][0]
        max_c = (max_l + max_r) / 2
        p_nose = points[16][0]

        tilt_rate = (p_nose - max_c) / (max_r - max_l)
        # print "tilt_rate", tilt_rate
        if math.fabs(tilt_rate) < 0.4:
            return True
        else:
            return False

    def isFrontFace_72(self, jsonrecorder):
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
    src_js='./json'
    src_imgPath='./image'
    out_Path='./output_eye'
    for root,dirs,files in os.walk(src_js):
        for ele in files:
            #if  ele.find('fix_fix')!=-1:
                key_id=root.split(os.sep)[-1]
                key_id=key_id[:-2]
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
                obj.Run_29()
