import json
import cv2
import os


def LoadJson(js_path):
    js_ctx = open(js_path,'r').readlines()
    return js_ctx

def GetFace(ele):
    ele = json.loads(ele)
    img_key = ele["image_key"]
    try:
        head_ctx =ele["head"]
        for i in head_ctx:
           if i['attrs']['ignore'] == 'no':
               if i['attrs']['smoke'] != 'no':
                   print 'there is smoke'
                   Is_smoke = True
               else:
                   Is_smoke = False
               face_pos =  i['data']
               #x1 y1 x2 y2
               width = int(face_pos[2])- int(face_pos[0])
               heigth = int(face_pos[3])- int(face_pos[1])
               roi_x1 = int(face_pos[0])#- width*0.25
               roi_y1 = int(face_pos[1])#- width*0.25
               roi_x2 = int(face_pos[2])#+ heigth*0.25
               roi_y2 = int(face_pos[3])#+ heigth*0.25
               roi_width = roi_x2 - roi_x1
               roi_heigth = roi_y2 - roi_y1
               return  int(roi_x1), int(roi_y1) , int(roi_width) ,int(roi_heigth),img_key,Is_smoke
           else:
               return  0,0,0,0,0,0
    except:
        print 'this line is wrong'
        return 0,0,0,0,0,0

def DrawImg(img_path,savePath,img_key,Is_phone,x,y,width ,heigth):
    file = img_path +os.sep +img_key
    frame = cv2.imread(file)
    if y < 0 or x < 0 or (x + width) > 1280 or (y + heigth) > 720:
        return
    sub = frame[y:y+heigth ,x:x+width]
    if  Is_phone == True:
        phone_save = savePath +os.sep +'phone'
        if not  os.path.exists(phone_save):
            os.makedirs(phone_save)
        if  len(sub) != 0 and len(sub[0]) != 0:
            tmp =phone_save +os.sep+img_key
            cv2.imwrite(tmp ,sub)
    if Is_phone == False:
        a_save = savePath +os.sep + 'normal'
        if not  os.path.exists(a_save):
            os.makedirs(a_save)
        if  len(sub) != 0 and len(sub[0]) != 0:
            tmp =a_save +os.sep+img_key
            cv2.imwrite(tmp ,sub)

def WalkDir(srcdir):
    list_dir = os.listdir(srcdir)
    list_dstdir = []
    name_list=[]
    for ele in list_dir:
        name= os.path.join(ele)
        name_list.append(name)
    return name_list






if __name__ == '__main__':
    num = 0
    src_js='/mnt/hgfs/Share/data/json'
    src_imgPath='/mnt/hgfs/Share/data/image'
    out_path='/mnt/hgfs/Share/data/output_face'
    for root,dirs,files in os.walk(src_js):
        for ele in files:
            key_id = root.split(os.sep)[-1]
            jspath = root+os.sep+ele
            print jspath
            imagePath = src_imgPath+os.sep +key_id
            print imagePath
            out_imagePath = out_path +os.sep +key_id
            print out_imagePath
            if not os.path.exists(out_imagePath):
                os.makedirs(out_imagePath)
            js_ctx = open(jspath,'r').readlines()
            for ele in js_ctx:
                # try:
                x,y,w,h,img_key,status = GetFace(ele)
                if status == True:
                    num = num +1
    print 'smoke num  is  ',num
               # if x != 0:
               #     DrawImg(imagePath ,out_imagePath,img_key,status,x,y,w,h)
               #     print out_imagePath+os.sep +img_key
               # else :
               #     print 'Be careful no head !!'
                # except:
                #     print ele

#    src_js='/mnt/hgfs/Share/data/json'
#    src_imgPath='/mnt/hgfs/Share/data/image'
#    out_path='/mnt/hgfs/Share/data/output_face'
#
#    jspath = '/mnt/hgfs/Share/data/json/11526/11526_1.json'
#    key_id = str(11526)
#    imagePath = src_imgPath+os.sep +key_id
#    out_imagePath = out_path +os.sep +key_id
#    if not os.path.exists(out_imagePath):
#                os.makedirs(out_imagePath)
#    js_ctx = open(jspath,'r').readlines()
#    ele = js_ctx[0]
#    # try:
#    x,y,w,h,img_key,status = GetFace(ele)
#    if x != 0:
#        DrawImg(imagePath ,out_imagePath,img_key,status,x,y,w,h)
#        print out_imagePath+os.sep +img_key



