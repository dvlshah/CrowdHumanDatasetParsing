__author__ = "Deval Shah"
__email__ = "devalshah190@gmail.com"

import json
import os
import sys
import argparse
import random
import cv2

dataset_dir = ""

"""
Function to read file in a list
@param : filename
"""
def read_file(filename):
    f =  open(filename)
    file_content = f.readlines()
    print("Total images in file %d " %(len(file_content)))
    return file_content

"""
Function to get image data information in a list
@param : file read in list

Each entry of list has n box entries per images 
where each box entry has following entries per box

visible_box : bbox coordinates of visible box 
full_box    : bbox coordinates of full box (annotator might have extrapolated if not seen fully)
head_box    : bbox coordinates of head box
occ         : whether it is occluded or not.
box_id      : Id of box in the image
unsure      : annotator marks it 0 if 100% sure
h_ignore    : head box that should be ignored if 1
h_occ       : head box occluded or not
h_unsure    : head box marked as 0 if 100% sure
tag         : class of box
"""
def getImageData(fcontent):
    attributes = []
    for line in range(len(fcontent)):
        temp     = fcontent[line]
        data     = json.loads(temp)
        img_id   = int(data['ID'].split(',')[0])
        img_hash = data['ID'].split(',')[1]
        box      = []

        #Ground Truth Boxes Dictionary
        gt_boxes = data["gtboxes"]
        #print("Image ID : %d | Image Hash : %s | No of boxes : %d" %(img_id,img_hash, len(gt_boxes)))
        
        for box_idx in range(len(gt_boxes)):
            #Visible Box
            visible_box = gt_boxes[box_idx]['vbox']
            #Full Box
            full_box    = gt_boxes[box_idx]['fbox']
            #Head Box
            head_box    = gt_boxes[box_idx]['hbox']

            #Extra Attributes
            extra     = gt_boxes[box_idx]['extra']
            if 'occ' in extra:
                occ  = extra['occ']
            else:
                occ  = -1

            if 'box_id' in extra:
                box_id = extra['box_id']
            else:
                box_id = -1

            if 'unsure' in extra:
                unsure = extra['unsure']
            else:
                unsure = -1
            
            #Head Attributes
            head_attr = gt_boxes[box_idx]['head_attr']
            if 'ignore' in head_attr:
                h_ignore = head_attr['ignore']
            else:
                h_ignore = -1

            if 'occ' in head_attr:
                h_occ = head_attr['occ']
            else:
                h_occ = -1

            if 'unsure' in head_attr:
                h_unsure = head_attr['unsure']
            else:
                h_unsure = -1
            
            #Tag
            tag  = gt_boxes[box_idx]['tag']
            #Single box info
            box.append([data['ID'],visible_box, full_box, head_box, occ, box_id, unsure, h_ignore, h_occ, h_unsure, tag])
        #All boxes per image
        attributes.append(box)
    return attributes

"""
Function to print information of box of image
@params
    image_info : 
"""
def display(image_info):
    image_id    = image_info[0]
    visible_box = image_info[1]
    full_box    = image_info[2]
    head_box    = image_info[3]
    occ         = image_info[4]
    box_id      = image_info[5]
    unsure      = image_info[6]
    h_ignore    = image_info[7]
    h_occ       = image_info[8]
    h_unsure    = image_info[9]
    tag         = image_info[10]
    print("Image ID  : %s" %(image_id))
    print("Box ID    : %d" %(box_id))
    print("Visible Box ",visible_box)
    print("Full Box ",full_box)
    print("Head box",head_box)
    print("%s | Occlusion : %d | Unsure : %d" %(tag,occ,unsure))
    print("Head   | Occlusion : %d | Unsure : %d | Ignore : %d" %(h_occ,h_unsure,h_ignore))

"""
Function to draw boxes on image
@params 
    img : cv2 image
    box : [xmin,ymin,xmax,ymax]
"""
def drawOnImage(img,box):
    visible_box = box[1]
    full_box    = box[2]
    head_box    = box[3]
    occ         = box[4]
    box_id      = box[5]
    unsure      = box[6]
    h_ignore    = box[7]
    h_occ       = box[8]
    h_unsure    = box[9]
    tag         = box[10]

    xmin = visible_box[0]
    ymin = visible_box[1]
    xmax = visible_box[0] + visible_box[2]
    ymax = visible_box[1] + visible_box[3]

    #if unsure == 0:
    cv2.rectangle(img, (xmin,ymin),(xmax,ymax), (0,255,0), 1)
    
    xmin = head_box[0]
    ymin = head_box[1]
    xmax = head_box[0] + head_box[2]
    ymax = head_box[1] + head_box[3]
    
    #if h_ignore == 0:
    cv2.rectangle(img, (xmin,ymin),(xmax,ymax), (255,0,0), 1)

    return img

"""
Function to check filepath's existence
@params 
    filepath : full path of file
"""
def check_file_presence(filepath):
    if os.path.isfile(filepath):
        return 1
    else:
        return 0

"""
Function to check image file path is from which directory
The train and test annotations file has paths from all dirs
@params
    image_path : path of image
"""
def check_image_path(image_path):
    train_01 = dataset_dir+"/CrowdHuman_train01"
    train_02 = dataset_dir+"/CrowdHuman_train02"
    train_03 = dataset_dir+"/CrowdHuman_train03"
    
    image_path_1 = train_01+"/"+image_path
    image_path_2 = train_02+"/"+image_path
    image_path_3 = train_03+"/"+image_path
    
    if check_file_presence(image_path_1):
        return image_path_1
    if check_file_presence(image_path_2):
        return image_path_2
    if check_file_presence(image_path_3):
        return image_path_3

"""
Function to debug the data retrieval functions
@param : 
    data : output of getImageData fn
"""
def debug(data):
    #In place shuffle
    random.shuffle(data)
    data = data[0:5]
    for image_info in data:
        print("##########################################################")
        print("No of boxes : %d" %(len(image_info)))
        image_name       = image_info[0][0]+".jpg"
        img_path         = check_image_path(image_name)
        img              = cv2.imread(img_path)
        height, width, _ = img.shape
        
        if height > 960: height = 960
        if width  > 1280: width = 1280

        for box in image_info:
            display(box)
            img  = drawOnImage(img,box)
        img = cv2.resize(img, (width, height))
        cv2.imshow("No of Boxes "+str(len(image_info)),img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description='CrowdHumanDatasetParsing')
    parser.add_argument('--annFile' ,type=str,
                        help='Annotation file name')
    parser.add_argument('--datasetDir', type=str,
                        help='Dataset directory')
    parser.add_argument('--debug', type=int,
                        help='Debug mode')
    args = parser.parse_args()
    return args

def main():
    args        = parse_args()
    
    global dataset_dir
    dataset_dir = args.datasetDir
    
    #Read annotation file
    fcontent = read_file(args.annFile)
    
    #Get all image bbox information
    dataInfo = getImageData(fcontent)
    
    if args.debug == 1:
        debug(dataInfo)
    
if __name__=="__main__":
    main()