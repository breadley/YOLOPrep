'''
////////////////////////////////////////////////////////////////////////////
//
//  This file is part of rt-ai
//
//  Copyright (c) 2018, richardstech
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy of
//  this software and associated documentation files (the "Software"), to deal in
//  the Software without restriction, including without limitation the rights to use,
//  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
//  Software, and to permit persons to whom the Software is furnished to do so,
//  subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
//  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
//  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
//  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
//  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
//  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Based on work from https://medium.com/@manivannan_data/how-to-train-yolov3-to-detect-custom-objects-ccbcafeb13d2
and code at https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool.

'''

import os
from os import walk, getcwd
from PIL import Image
import sys

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

if len(sys.argv) != 2:
    print('Usage is: python convert.py <projname>')
    exit(1)

projName = sys.argv[1]
imagesPath = os.path.join(projName, 'Images')
datasetPath = os.path.join(projName, 'Dataset')
weightsPath = os.path.join(projName, 'Weights')

if not os.path.exists(imagesPath):
    print('Images directory does not exist')
    exit(1)

cls_id = 0
wd = getcwd()
counter = 1
percentage_test = 20
index_test = round(100 / percentage_test)  
file_train = open(os.path.join(projName, 'train.txt'), 'w')  
file_test = open(os.path.join(projName, 'test.txt'), 'w')

while True:
    imageDir = os.path.join(imagesPath, str(cls_id))
    if not os.path.exists(imageDir):
        break

    """ Get input text file list """
    txt_name_list = []
    for (dirpath, dirnames, filenames) in walk(imageDir):
        txt_name_list.extend(filenames)
        break
    print(txt_name_list)
    """ Process """
    for txt_name in txt_name_list:
        if not txt_name.endswith('.txt'):
            continue
            
        """ Open input text files """
        txt_path = os.path.join(imageDir, txt_name)
        print("Input:" + txt_path)
        txt_file = open(txt_path, "r")
        lines = txt_file.read().split('\n') 

        """ Open output text files """
        txt_outpath = os.path.join(datasetPath, txt_name)
        print("Output:" + txt_outpath)
        txt_outfile = open(txt_outpath, "w")


        """ Convert the data to YOLO format """
        ct = 0
        print(lines)
        for line in lines:
            elems = line.split(' ')
            print(elems)
            if(len(elems) >= 2):
                ct = ct + 1
                print(line + "\n")
                elems = line.split(' ')
                print(elems)
                xmin = elems[0]
                xmax = elems[2]
                ymin = elems[1]
                ymax = elems[3]
                print(elems[0])
                #
                img_load_path = os.path.join(imageDir, str('%s.jpg'%(os.path.splitext(txt_name)[0])))
                img_save_path = os.path.join(datasetPath, str('%s.jpg'%(os.path.splitext(txt_name)[0])))
                print(img_load_path)
                #t = magic.from_file(img_path)
                #wh= re.search('(\d+) x (\d+)', t).groups()
                im=Image.open(img_load_path)
                im.save(img_save_path)
                w= int(im.size[0])
                h= int(im.size[1])
                #w = int(xmax) - int(xmin)
                #h = int(ymax) - int(ymin)
                # print(xmin)
                print(w, h)
                print(float(xmin), float(xmax), float(ymin), float(ymax))
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert((w,h), b)
                print(bb)
                txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

        """ Save those images with bb into list"""
        if(ct != 0):
            if counter == index_test:
                counter = 1
                file_test.write('%s/%s/%s.jpg\n'%(wd, datasetPath, os.path.splitext(txt_name)[0]))
            else:
                counter += 1
                file_train.write('%s/%s/%s.jpg\n'%(wd, datasetPath, os.path.splitext(txt_name)[0]))
               
    cls_id += 1

file_train.close()
file_test.close()
print ('Processed {} classes in project {}'.format(cls_id, sys.argv[1]))
