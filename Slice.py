# -*- coding:UTF-8 -*-
import os
import sys
import cv2

#_scriptDir_ = os.path.dirname(__file__)
#_scriptName_ = os.path.basename(__file__)
#os.chdir(_scriptDir_)
#sys.path.append(_scriptDir_)

def WalkDir(srcdir):
    list_dir = os.listdir(srcdir)#枚举出当前目录下的所有单位（包括目录和文件），具有不穿透目录的特性
    list_dstdir = []# 定义空白列表用以承载
    list_file = []
    for ele in list_dir:
        abPath = os.path.join(srcdir, ele).replace('/', os.sep).replace('\\', os.sep)
        if os.path.isdir(abPath):#判断list_dir中所有单位是否是目录，如果是，进入下一层函数
            list_dstdir.append(abPath)#将本层所有是目录的单位存入list_dstdir中
            #list_dstdir = list_dstdir + WalkDir(abPath)#将下一层所有是目录的单位存入list_dstdir
            list_file =list_file + WalkDir(abPath)#将下一层所有是目录的单位存入list_dstdir
        else:
            list_file.append(abPath)

            #此句是递归的部分，将每一层的目录结果返回
    return list_file



if __name__ == '__main__':
    l = WalkDir(sys.argv[1])
    for ele in l:
        videoCap = cv2.VideoCapture(ele)
        videoPath = os.path.dirname(ele)
        videoID = os.path.basename(ele).replace(".mp4","_img")
        imageSavePath = os.path.join(videoPath,videoID)
        try:
            step = int(sys.argv[2])
        except:
            step = 1
        os.makedirs(imageSavePath)
        frameCount = int(videoCap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        print "Sum = ",frameCount

        if step == 1:
            for i in range(0,frameCount):
                ret,frame = videoCap.read()
                if ret:
                    cv2.imwrite(os.path.join(imageSavePath,str(i) + ".png"),frame)
                    print videoID + str(i) + ".png"
                else:
                    print "read error"
        else:
            for i in range(0,frameCount,step):
                videoCap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,i)
                ret,frame = videoCap.read()
                if ret:
                    cv2.imwrite(os.path.join(imageSavePath, str(i) + ".png"),frame)
                    print videoID + str(i) + ".png"
                else:
                    print "read error"
