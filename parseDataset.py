__author__ = "Deval Shah"
__email__ = "devalshah190@gmail.com"

import json
import os
import sys
import argparse
import random
import cv2

dataset_dir = ""
train       = 0

"""
Function to read file in a list
@params
    filename : Path of file you want to read in the list python
"""
def readFile(filename):
    f =  open(filename)
    file_content = f.readlines()
    print("Total images in file %d" %(len(file_content)))
    return file_content

"""
Function to filter the data based on the attributes provided in the config file
@params
        b1 : Box attributes defined in config file
        b2 : box entry from annotation file

The idea is to get bbox info from images based on the need of the user.Some people
may not want the occluded or ignore region boxes from dataset. This can be filtered
based on what you provide in config file. 

For eg : h_occ = 1 in config file means you want occluded head to considered as valid 
data while parsing and vice versa for h_occ = 0
"""

def checkValidity(b1,b2):
    if ( (b1['tag'] == b2[10] and int(b1['unsure']) == b2[6]) or (int(b1['occ']) == b2[4]) ):
        if(int(b1['visible']) == 0): 
            b2[1] = [0,0,0,0]
        if(int(b1['full']) == 0):
            b2[2] = [0,0,0,0]
    else:
        b2[1] = [0,0,0,0]
        b2[2] = [0,0,0,0]

    if(int(b1['head']) == 1):
        if ( (int(b1['h_ignore']) == b2[7] and int(b1['h_unsure']) == b2[9]) ) or (int(b1['h_occ']) == b2[8]):
            return b2
        else:
            b2[3] = [0,0,0,0]
    else:
        b2[3] = [0,0,0,0]
    
    return b2

"""
Function to get image data information in a list
@param 
    fcontent       : file read in list
    box_attributes : type of boxes you want in dataset

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
def getImageData(fcontent,box_attributes):
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
            print(extra)
            if 'occ' in extra:
                occ  = extra['occ']

            if 'box_id' in extra:
                box_id = extra['box_id']

            if 'unsure' in extra:
                unsure = extra['unsure']
            else:
                unsure = 1
            
            #Head Attributes
            head_attr = gt_boxes[box_idx]['head_attr']
            if 'ignore' in head_attr:
                h_ignore = head_attr['ignore']

            if 'occ' in head_attr:
                h_occ = head_attr['occ']

            if 'unsure' in head_attr:
                h_unsure = head_attr['unsure']
            
            #Tag
            tag  = gt_boxes[box_idx]['tag']
            #Single box info
            temp = [data['ID'],visible_box, full_box, head_box, occ, box_id, unsure, h_ignore, h_occ, h_unsure, tag]
            temp1 = checkValidity(box_attributes,temp)
            print(temp1)
            box.append(temp1)
        #All boxes per image
        attributes.append(box)
    return attributes

"""
Function to print information of box of image
@params
    image_info : BBOX information along with meta data like occlusion, ignore, unsure flags
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
    print("$"*40)
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
    
    if(visible_box[2] != 0):
        xmin = visible_box[0]
        ymin = visible_box[1]
        xmax = visible_box[0] + visible_box[2]
        ymax = visible_box[1] + visible_box[3]

        cv2.rectangle(img, (xmin,ymin),(xmax,ymax), (255,0,0), 1)
    
    if(head_box[2] != 0):
        xmin = head_box[0]
        ymin = head_box[1]
        xmax = head_box[0] + head_box[2]
        ymax = head_box[1] + head_box[3]
        
        #if h_ignore == 0:
        cv2.rectangle(img, (xmin,ymin),(xmax,ymax), (0,255,0), 1)
    
    if(full_box[2] != 0):
        xmin = full_box[0]
        ymin = full_box[1]
        xmax = full_box[0] + full_box[2]
        ymax = full_box[1] + full_box[3]
        
        #if h_ignore == 0:
        cv2.rectangle(img, (xmin,ymin),(xmax,ymax), (0,0,0), 1)

    return img

"""
Function to check filepath's existence
@params 
    filepath : full path of file
"""
def checkFilePresence(filepath):
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
def checkImagePath(image_path):
    train_01 = dataset_dir+"/CrowdHuman_train01"
    train_02 = dataset_dir+"/CrowdHuman_train02"
    train_03 = dataset_dir+"/CrowdHuman_train03"
    
    #train
    image_path_1 = train_01+"/"+image_path
    image_path_2 = train_02+"/"+image_path
    image_path_3 = train_03+"/"+image_path
    
    #test
    val_01       = dataset_dir+"/CrowdHuman_val"
    image_path_4 = val_01+"/"+image_path
    test_01      = dataset_dir+"/CrowdHuman_test"
    image_path_5 = test_01+"/"+image_path

    if train == 1:
        if checkFilePresence(image_path_1):
            return image_path_1
        if checkFilePresence(image_path_2):
            return image_path_2
        if checkFilePresence(image_path_3):
            return image_path_3
    else:
        if checkFilePresence(image_path_4):
            return image_path_4
        if checkFilePresence(image_path_5):
            return image_path_5

"""
Function to debug the data retrieval functions
@param : 
    data : output of getImageData fn
"""
def debug(data,no_of_images):
    #In place shuffle
    random.shuffle(data)
    data = data[0:no_of_images]
    for image_info in data:
        print("#"*60)
        print("No of boxes : %d" %(len(image_info)))
        image_name       = image_info[0][0]+".jpg"
        print(image_name)
        img_path         = checkImagePath(image_name)
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
"""
Function to get config data from given config file path 
in a dictionary
@params
    config_file_path : Path to config file
"""
def getConfigData(config_file_path):
    import configparser
    config = configparser.RawConfigParser()
    config.read(config_file_path)
    config_dict = {}
    config_dict['box_attributes'] = dict(config.items('box_attributes'))
    config_dict['dataset']        = dict(config.items('dataset'))
    config_dict['test']           = dict(config.items('test'))
    return config_dict

def parseArgs():
    parser = argparse.ArgumentParser(description='CrowdHumanDatasetParsing')
    parser.add_argument('--config_file_path', type=str,
                        help='Path to config file')
    parser.add_argument('--data',type=str,
                        help='To read annotation for train/test data.\
                        "train" or "test"')
    args = parser.parse_args()
    return args

def main():
    global dataset_dir,train 
    
    args           = parseArgs()
    config_dict    = getConfigData(args.config_file_path)

    box_attributes = config_dict['box_attributes']
    dataset        = config_dict['dataset']
    dataset_dir    = dataset['dataset_base_dir']
    
    debug_flag     = int(config_dict['test']['debug'])
    no_of_images   = int(config_dict['test']['num_images'])

    #Read annotation file
    if args.data == "train":
        train    = 1
        fcontent = readFile(dataset['train_annotation_file_path'])
    else:
        train    = 0
        fcontent = readFile(dataset['test_annotation_file_path'])
    
    #Get all image bbox information
    dataInfo = getImageData(fcontent,box_attributes)
    
    #Debug the code by plotting bbox on random images from dataset
    if debug_flag == 1:
        debug(dataInfo,no_of_images)
    
if __name__=="__main__":
    main()
