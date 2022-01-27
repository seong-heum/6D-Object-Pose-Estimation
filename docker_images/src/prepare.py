import sys
import os
from shutil import copyfile

import math
import numpy as np
import cv2 as cv
import json
import random
from utils import *
from MeshPly import MeshPly

if __name__ == '__main__':

    if len(sys.argv) == 2:
        print("ID: {}".format(sys.argv[1]))
        oname = sys.argv[1]
        dname = "datasets"
        imgWidth = 1280
        imgHeight = 720
        if(os.path.isdir("data/")==0): os.mkdir("data")
        if(os.path.isdir("data/" + oname)==0): os.mkdir("data/" + oname)
        if(os.path.isdir("data/" + oname + "/models")==0): os.mkdir("data/" + oname + "/models")
        if(os.path.isdir("data/" + oname + "/images")==0): os.mkdir("data/" + oname + "/images")
        # if(os.path.isdir("data/" + oname + "/check")==0): os.mkdir("data/" + oname + "/check")
        if(os.path.isdir("data/" + oname + "/labels")==0): os.mkdir("data/" + oname + "/labels")
        if(os.path.isdir("data/" + oname + "/masks")==0): os.mkdir("data/" + oname + "/masks")
        if(os.path.isdir("data/" + oname + "/cams")==0): os.mkdir("data/" + oname + "/cams")

        # CNN model
        mname = "data/" + oname + '/models/' + "yolo-pose.cfg"
        copyfile(dname + '/' + "models/" + "yolo-pose.cfg", mname)

        # 3D model
        mname = "data/" + oname + '/' + oname + ".ply"
        copyfile(dname + '/' + oname + ".3D_Shape/" + oname + ".ply", mname)
        mesh = MeshPly(mname)
        vertices = np.c_[np.array(mesh.vertices), np.ones((len(mesh.vertices), 1))].transpose()
        corners3D = get_3D_corners(vertices)

        # load masks
        maskDir = dname + '/' + oname + ".Mask"
        maskExt = ".png"
        maskList = [_ for _ in os.listdir(maskDir) if _.endswith(maskExt)]

        for i in maskList:
            mask = cv.imread(maskDir + "/" + i, 0)
            if ((mask.shape[0] == imgHeight) & (mask.shape[1] == imgWidth)) == 0:
                print("mask size: {}\n".format(i))
                mask_ = cv.resize(mask, dsize=(imgWidth, imgHeight), interpolation=cv.INTER_CUBIC)
            else:
                mask_ = mask
            mask_rgb = cv.merge((mask_, mask_, mask_))
            cv.imwrite("data/" + oname + "/masks/" + i[-21:-6] + ".png", mask_rgb)

        maskDir = "data/" + oname + "/masks"
        imgList = [_ for _ in os.listdir(maskDir) if _.endswith(maskExt)]

        # load images
        imgDir = dname + '/' + oname + ".Images"
        imgExt = ".png"

        n = len(imgList)
        fx_, fy_, u0_, v0_ = [0, 0, 0, 0]
        for i in imgList:
            # image size
            imgName = imgDir + '/' + i
            image = cv.imread(imgName, 1)
            if((image.shape[0]==imgHeight)&(image.shape[1]==imgWidth))==0:
                print("image size: {}\n".format(i))
                image_resize = cv.resize( image, dsize=(imgWidth,imgHeight), interpolation=cv.INTER_CUBIC )
                cv.imwrite("data/" + oname + "/images/" + i, image_resize)
            else: copyfile(imgName, "data/" + oname + "/images/" + i)

            jname = dname + '/' + oname + '.3D_json/' + i[-21:-4] + '.json'
            fp = open(jname, 'rt', encoding='UTF8')
            jdata = json.load(fp)
            fx = float(jdata['metaData']['Fx'])
            fy = float(jdata['metaData']['Fy'])
            u0 = float(jdata['metaData']['PPx'])
            v0 = float(jdata['metaData']['PPy'])
            [fx_, fy_, u0_, v0_] = [fx_+fx/n, fy_+fy/n, u0_+u0/n, v0_+v0/n]
            #print(fx_, fy_, u0_, v0_)
            pts = jdata['labelingInfo'][0]['3DBox']['location'][0]
            fp.close()

            # camera parameters
            fc = open("data/" + oname + "/cams/" + i[-21:-4] + ".txt", 'w')
            fc.write("{} {} {} {}".format(fx, fy, u0, v0))
            fc.close()

            # cube annotations
            if( (0<float(pts['x9'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x9']=1
            if( (0<float(pts['y9'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y9']=1
            if( (0<float(pts['x4'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x4']=1
            if( (0<float(pts['y4'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y4']=1
            if( (0<float(pts['x1'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x1']=1
            if( (0<float(pts['y1'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y1']=1
            if( (0<float(pts['x8'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x8']=1
            if( (0<float(pts['y8'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y8']=1
            if( (0<float(pts['x5'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x5']=1
            if( (0<float(pts['y5'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y5']=1
            if( (0<float(pts['x3'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x3']=1
            if( (0<float(pts['y3'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y3']=1
            if( (0<float(pts['x2'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x2']=1
            if( (0<float(pts['y2'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y2']=1
            if( (0<float(pts['x7'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x7']=1
            if( (0<float(pts['y7'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y7']=1
            if( (0<float(pts['x6'])/imgWidth)      )==0: print("cube loc. check1: {}\n".format(i)); pts['x6']=1
            if( (0<float(pts['y6'])/imgHeight)     )==0: print("cube loc. check1: {}\n".format(i)); pts['y6']=1
            if( (0<float(pts['x-range'])/imgWidth) )==0: print("cube loc. check1: {}\n".format(i)); pts['x-range']=1
            if( (0<float(pts['y-range'])/imgHeight))==0: print("cube loc. check1: {}\n".format(i)); pts['y-range']=1
            if( (1>float(pts['x9'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x9']=imgWidth-1
            if( (1>float(pts['y9'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y9']=imgHeight-1
            if( (1>float(pts['x4'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x4']=imgWidth-1
            if( (1>float(pts['y4'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y4']=imgHeight-1
            if( (1>float(pts['x1'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x1']=imgWidth-1
            if( (1>float(pts['y1'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y1']=imgHeight-1
            if( (1>float(pts['x8'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x8']=imgWidth-1
            if( (1>float(pts['y8'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y8']=imgHeight-1
            if( (1>float(pts['x5'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x5']=imgWidth-1
            if( (1>float(pts['y5'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y5']=imgHeight-1
            if( (1>float(pts['x3'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x3']=imgWidth-1
            if( (1>float(pts['y3'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y3']=imgHeight-1
            if( (1>float(pts['x2'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x2']=imgWidth-1
            if( (1>float(pts['y2'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y2']=imgHeight-1
            if( (1>float(pts['x7'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x7']=imgWidth-1
            if( (1>float(pts['y7'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y7']=imgHeight-1
            if( (1>float(pts['x6'])/imgWidth)      )==0: print("cube loc. check2: {}\n".format(i)); pts['x6']=imgWidth-1
            if( (1>float(pts['y6'])/imgHeight)     )==0: print("cube loc. check2: {}\n".format(i)); pts['y6']=imgHeight-1
            if( (1>float(pts['x-range'])/imgWidth) )==0: print("cube loc. check2: {}\n".format(i)); pts['x-range']=imgWidth-1
            if( (1>float(pts['y-range'])/imgHeight))==0: print("cube loc. check2: {}\n".format(i)); pts['y-range']=imgHeight-1
            fc = open("data/" + oname + "/labels/" + i[-21:-4] + ".txt", 'w')
            fc.write('0 ')
            fc.write("{:.6} ".format(float(pts['x9'])/1280))
            fc.write("{:.6} ".format(float(pts['y9'])/720))
            fc.write("{:.6} ".format(float(pts['x4'])/1280))
            fc.write("{:.6} ".format(float(pts['y4'])/720))
            fc.write("{:.6} ".format(float(pts['x1'])/1280))
            fc.write("{:.6} ".format(float(pts['y1'])/720))
            fc.write("{:.6} ".format(float(pts['x8'])/1280))
            fc.write("{:.6} ".format(float(pts['y8'])/720))
            fc.write("{:.6} ".format(float(pts['x5'])/1280))
            fc.write("{:.6} ".format(float(pts['y5'])/720))
            fc.write("{:.6} ".format(float(pts['x3'])/1280))
            fc.write("{:.6} ".format(float(pts['y3'])/720))
            fc.write("{:.6} ".format(float(pts['x2'])/1280))
            fc.write("{:.6} ".format(float(pts['y2'])/720))
            fc.write("{:.6} ".format(float(pts['x7'])/1280))
            fc.write("{:.6} ".format(float(pts['y7'])/720))
            fc.write("{:.6} ".format(float(pts['x6'])/1280))
            fc.write("{:.6} ".format(float(pts['y6'])/720))
            fc.write("{:.6} ".format(float(pts['x-range'])/1280))
            fc.write("{:.6} ".format(float(pts['y-range'])/720))
            fc.close()

            # check
            #x1 = float(pts['x4'])
            #y1 = float(pts['y4'])
            #x2 = float(pts['x1'])
            #y2 = float(pts['y1'])
            #x3 = float(pts['x8'])
            #y3 = float(pts['y8'])
            #x4 = float(pts['x5'])
            #y4 = float(pts['y5'])
            #x5 = float(pts['x3'])
            #y5 = float(pts['y3'])
            #x6 = float(pts['x2'])
            #y6 = float(pts['y2'])
            #x7 = float(pts['x7'])
            #y7 = float(pts['y7'])
            #x8 = float(pts['x6'])
            #y8 = float(pts['y6'])
            #cv.line(image, (int(x1), int(y1)), (int(x1), int(y1)), [0, 255, 0], 10)
            #cv.line(image, (int(x2), int(y2)), (int(x2), int(y2)), [0, 255, 0], 10)
            #cv.line(image, (int(x3), int(y3)), (int(x3), int(y3)), [0, 255, 0], 10)
            #cv.line(image, (int(x4), int(y4)), (int(x4), int(y4)), [0, 255, 0], 10)
            #cv.line(image, (int(x5), int(y5)), (int(x5), int(y5)), [0, 255, 0], 10)
            #cv.line(image, (int(x6), int(y6)), (int(x6), int(y6)), [0, 255, 0], 10)
            #cv.line(image, (int(x7), int(y7)), (int(x7), int(y7)), [0, 255, 0], 10)
            #cv.line(image, (int(x8), int(y8)), (int(x8), int(y8)), [0, 255, 0], 10)
            #cv.line(image, (int(x1), int(y1)), (int(x2), int(y2)), [0, 255, 0], 2)
            #cv.line(image, (int(x1), int(y1)), (int(x3), int(y3)), [0, 255, 0], 2)
            #cv.line(image, (int(x2), int(y2)), (int(x4), int(y4)), [0, 255, 0], 2)
            #cv.line(image, (int(x3), int(y3)), (int(x4), int(y4)), [0, 255, 0], 2)
            #cv.line(image, (int(x5), int(y5)), (int(x6), int(y6)), [0, 255, 0], 2)
            #cv.line(image, (int(x5), int(y5)), (int(x7), int(y7)), [0, 255, 0], 2)
            #cv.line(image, (int(x6), int(y6)), (int(x8), int(y8)), [0, 255, 0], 2)
            #cv.line(image, (int(x7), int(y7)), (int(x8), int(y8)), [0, 255, 0], 2)
            #cv.line(image, (int(x1), int(y1)), (int(x5), int(y5)), [0, 255, 0], 2)
            #cv.line(image, (int(x2), int(y2)), (int(x6), int(y6)), [0, 255, 0], 2)
            #cv.line(image, (int(x3), int(y3)), (int(x7), int(y7)), [0, 255, 0], 2)
            #cv.line(image, (int(x4), int(y4)), (int(x8), int(y8)), [0, 255, 0], 2)
            #cv.putText(image, '1', (int(x1) + 10, int(y1) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #cv.putText(image, '2', (int(x2) + 10, int(y2) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #cv.putText(image, '3', (int(x3) + 10, int(y3) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #cv.putText(image, '4', (int(x4) + 10, int(y4) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #cv.putText(image, '5', (int(x5) + 10, int(y5) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #cv.putText(image, '6', (int(x6) + 10, int(y6) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #cv.putText(image, '7', (int(x7) + 10, int(y7) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #cv.putText(image, '8', (int(x8) + 10, int(y8) + 10), cv.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
            #check = "data/" + oname + "/check/" + i[-21:-4] + ".jpg"
            #cv.imwrite(check, image)

        # train, test list
        randind = random.sample(range(1, 1 + len(imgList)), len(imgList))
        sample10 = int(len(imgList) / 10)
        sample20 = int(sample10 * 2)

        fo = open("data/" + oname + '/' + "test.txt", 'w')
        cnt = 0
        for i in randind[0:sample20]:
            fo.write('data/' + oname + '/images/' + imgList[i - 1] + '\n')
            cnt = cnt + 1
        fo.close()

        fo = open("data/" + oname + '/' + "train.txt", 'w')
        cnt = 0
        for i in randind[sample20:]:
            fo.write('data/' + oname + '/images/' + imgList[i - 1] + '\n')
            cnt = cnt + 1
        fo.close()

        # training data
        fo = open("data/" + oname + '/' + oname + ".data", 'w')
        fo.write("train = data/{}/train.txt\n".format(oname))
        fo.write("valid = data/{}/test.txt\n".format(oname))
        fo.write("backup = data/{}/models\n".format(oname))
        fo.write("mesh = data/{}/{}.ply\n".format(oname, oname))
        fo.write("name = {}\n".format(oname))
        fo.write("gpus = 0\n")
        fo.write("width = {}\n".format(imgWidth))
        fo.write("height = {}\n".format(imgHeight))
        fo.close()
    else:
        print(">> prepare [ID]")