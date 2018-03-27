import json
import cv2
import os


def LoadJson(js_path):
    js_ctx = open(js_path,'r').readlines()
    return js_ctx

def WalkDir(srcdir):
    list_dir = os.listdir(srcdir)
    list_dstdir = []
    name_list=[]
    for ele in list_dir:
        name= os.path.join(ele)
        name_list.append(name)
    return name_list

def changejs(out_jspath ,ele):
    file = open(out_jspath,'a')
    ctx = json.dumps(ele)+'\n'
    file.write(ctx)
    file.close

def mvimg(src_path ,key_id , out_path ,img_key):
    out_imgpath = out_path +os.sep+ 'Image'+os.sep+key_id
    #print src_path+os.sep +key_id+os.sep+img_key
    if not os.path.exists(out_imgpath):
        os.makedirs(out_imgpath)
    cmd = 'cp '+ src_path+os.sep +key_id+os.sep+img_key +' '+out_imgpath
    #print out_imgpath
    #print cmd
    os.system(cmd)




if __name__ == '__main__':
    src_js='/mnt/hgfs/Share/data/json'
    src_imgPath='/mnt/hgfs/Share/data/image'
    out_path='/mnt/hgfs/Share/data/output_phone'
    out_jspath = out_path +os.sep+ 'Anno'
    for root,dirs,files in os.walk(src_js):
        for ele in files:
            key_id = root.split(os.sep)[-1]
            jspath = root+os.sep+ele
            #print jspath
            imagePath = src_imgPath+os.sep +key_id
            #print imagePath
            out_imagePath = out_path +os.sep +key_id
            #print out_imagePath
            out_subjs = out_jspath + os.sep +key_id +'.json'
        #   if not os.path.exists(out_imagePath):
         #       os.makedirs(out_imagePath)
            if not os.path.exists(out_jspath):
                os.makedirs(out_jspath)
            print out_subjs
            file = open(out_subjs,'w')
            js_ctx = open(jspath,'r').readlines()
            for ele in js_ctx:
                # try:
                ele = json.loads(ele)
                #print ele
                if ele.has_key("common_box"):
                    key = ele['image_key']
                    changejs(out_subjs ,ele)
                    mvimg(src_imgPath ,key_id, out_path,key)
                else :
                    print ele["image_key"],'this image dont  have phone'
            break    # except:
                #     print ele



