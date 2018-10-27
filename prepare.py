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
import sys


if len(sys.argv) != 3:
    print('Usage is: python prepare.py <projname> <class_count>')
    exit(1)
    
projName = sys.argv[1]
classCount = int(sys.argv[2])

imagesPath = os.path.join(projName, 'Images')
datasetPath = os.path.join(projName, 'Dataset')
weightsPath = os.path.join(projName, 'Weights')

# create project directory

if not os.path.exists(projName):
    os.mkdir(projName)

# create images subdirectory

if not os.path.exists(imagesPath):
    os.mkdir(imagesPath)

# create the class image directories for each class

for classIndex in range(classCount):
    classPath = os.path.join(imagesPath, str(classIndex))
    if not os.path.exists(classPath):
        os.mkdir(classPath)

# create Weights subdirectory

if not os.path.exists(weightsPath):
    os.mkdir(weightsPath)

# create Dataset subdirectory

if not os.path.exists(datasetPath):
    os.mkdir(datasetPath)
    
# create data file

cd = getcwd()
absProjDir = os.path.join(cd, projName)
trainDataPath = os.path.join(absProjDir, projName + '.data')

file_data = open(trainDataPath, 'w')  
file_data.write('classes={}\n'.format(classCount))
file_data.write('train={}\n'.format(os.path.join(absProjDir, 'train.txt')))
file_data.write('valid={}\n'.format(os.path.join(absProjDir, 'test.txt')))
file_data.write('names={}\n'.format(os.path.join(absProjDir, projName + '.names')))
file_data.write('backup={}\n'.format(os.path.join(absProjDir, 'Weights')))
file_data.close()

# create train.sh file

trainScriptPath = os.path.join(absProjDir, projName + '.sh')

file_data = open(trainScriptPath, 'w')  
file_data.write('./darknet detector train {} {} darknet53.conv.74'.format(trainDataPath, os.path.join(absProjDir, projName + '.cfg')))
file_data.close()
os.chmod(trainScriptPath, 0777)


print('Created project {} with {} classes'.format(projName, classCount))
