# CrowdHuman Dataset Parsing
This repo contains script to read the crowd human dataset in a structured format

# Getting Started
```
python3 parseDataset.py --config_file_path=./config.txt --data test

```
How to define config file for your requirements 

[dataset]
dataset_base_dir            path to directory where dataset folders are present after downloading
train_annotation_file_path  path to train annotation file
test_annotation_file_path   path to test annotation file


[box_attributes]
visible=1   will allow visible bbox. <br />
full=1      will allow full box.
head=1      will allow head box
occ=1       will allow occluded bboxes
unsure=0    will not allow unsure bboxes
h_ignore=0  will not allow ignored region bboxes
h_occ=0     will not allow occluded heads
h_unsure=0  will not allow unsure head bboxes
tag=person  will allow only bboxes with tag of person (other is mask)

[test]
debug=1     to debug by plotting bbox on below mentioned 'num_image' random images
num_images=5

The dataset download link is mentioned in the website mentioned below.

[Crowd Human Dataset Website](https://www.crowdhuman.org/)

[Crowd Human Dataset Paper Link](https://arxiv.org/pdf/1805.00123.pdf)

## Requirements

1. OpenCV : ```pip install opencv-python```
