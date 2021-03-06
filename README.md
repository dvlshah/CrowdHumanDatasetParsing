# CrowdHuman Dataset Parsing
This repo contains script to read the crowd human dataset in a structured format

# Getting Started
```
python3 parseDataset.py --config_file_path=./config.txt --data test

```
# How to define config file for your requirements 

[dataset] <br />
dataset_base_dir            path to directory where dataset folders are present after downloading <br />
train_annotation_file_path  path to train annotation file <br />
test_annotation_file_path   path to test annotation file <br />

<br />

[box_attributes] <br />
visible=1   will allow visible bbox. <br />
full=1      will allow full box. <br />
head=1      will allow head box <br />
occ=1       will allow occluded bboxes. <br />
unsure=0    will not allow unsure bboxes. <br />
h_ignore=0  will not allow ignored region bboxes. <br />
h_occ=0     will not allow occluded heads. <br />
h_unsure=0  will not allow unsure head bboxes. <br />
tag=person  will allow only bboxes with tag of person (other is mask). <br />

<br />

[test] <br />
debug=1     to debug by plotting bbox on below mentioned 'num_image' random images <br />
num_images=5 <br />

The dataset download link is mentioned in the website mentioned below.

[Crowd Human Dataset Website](https://www.crowdhuman.org/)

[Crowd Human Dataset Paper Link](https://arxiv.org/pdf/1805.00123.pdf)

## Requirements

1. OpenCV : ```pip install opencv-python```
