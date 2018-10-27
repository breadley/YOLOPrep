# How to Train Custom YOLOv3

## Introduction

These Python scripts create a directory structure for custom YOLOv3 training data. In the descriptions, "projname" should be replaced with the actual project name. "classcount" should also be replaced with the number of classes to be recognized.

MIT license.

## Download initial model

Get the darknet53 model from https://pjreddie.com/media/files/darknet53.conv.74. Place it in the Darknet root directory.

## Prepare the directory

Go to a suitable root folder for the training data. Copy prepare.py, bbox.py and convert.py into it. Then set that as the working directory and execute:

```
python prepare.py projname classcount
```

This creates the required directory structure within a directory projname. Within that, a subdirectory called Images is created along with a subdirectory in that for all the classes called Images/0, Images/1 etc. This is where the .jpg files for the class images should be placed.

A subdirectory called Dataset is generated. This will be used to store the data actually used for training.

## Config file

### yolov3-tiny.cfg

Line 3: Change batch size to something usefile like 4 or 8 (batch=4 or batch=8)

Line 4: Set subdivision size so sub-batch fits in GPU memory (subdivisions=2 or subdivisions=4 for example)

Line 127: Set filters=(classes + 5) * 3. This would be filters = 21 for 2 classes.

Line 135: Set classes=2.

Line 171: Set filters=(classes + 5) * 3. This would be filters = 21 for 2 classes.

Line 177: Set classes=2.

Save the file with the name projname.cfg in the projname directory.


### yolov3.cfg

yolo-obj.cfg is a 2 class version of yolov3.cfg. To convert yolov3.cfg for any number of classes do:

Line 3: Change batch size to something usefile like 4 or 8 (batch=4 or batch=8)

Line 4: Set subdivision size so sub-batch fits in GPU memory (subdivisions=2 or subdivisions=4 for example)

Line 603: Set filters=(classes + 5) * 3. This would be filters = 21 for 2 classes.

Line 610: Set classes=2.

Line 689: Set filters=(classes + 5) * 3. This would be filters = 21 for 2 classes.

Line 696: Set classes=2.

Line 776: Set filters=(classes + 5) * 3. This would be filters = 21 for 2 classes.

Line 783: Set classes=2.

Save the file with the name projname.cfg in the projname directory.

## projname/projname.names

Edit this file and put a name for each class on a separate line. Line 0 has the name for class0, line 1 has the name for class 1 etc. For example:

```
left_controller
right_controller
```

would be the contents if class 0 is left_controller and class 1 is right controller.

## Image preparation

The image files have to be of reasonable size (say 1024 pixels wide x 720 high) and with a .jpg extension. If not, there is a utility script called imageprep.sh that can be used to fix this. It is set up for a Sony RX100 but that can be changed of course.

Initially, copy all images for a class (keep backups!) into a temporary folder Temp in the root directory. Assuming they are from the Sony, run:

```
./imageprep.sh 
```
in the root directory. This resizes the images to 1024 pixels wide and changes the extensions to .jpg. Now copy the images to the appropriate folder for the class (e.g Images/0 for class 0). Do this for all classes.

## Bounding box generation

Run the following from the root directory:

```
python bbox.py projname
```
Enter the class name (e.g. 0) as the Image Dir. The first image should then appear. Draw boxes for all images. This creates text files in projname/Images/0 or whatever is appropriate. Do this for each class.

## Conversion to Darknet format

Run the following:

```
python convert.py projname
```

This populates the projname/Dataset directory and also create the other files needed for training.

## Training

Copy the projname/projname.sh script into the Darknet root directory, make the Darknet root directory the current directory and enter:

```
./projname.sh
```
This will create trained weight files in projname/Weights.





