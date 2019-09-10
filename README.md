# CrowdHuman Dataset Parsing
This repo contains script to read the crowd human dataset in a structured format

```
python parseDataset.py --annFile annotation_train.odgt --debug 0
```
Flags 

1. annFile = path to annotation file
2. debug   = flag (0 or 1) to display bounding box on five random images from dataset.

When debug mode is 1, you need the images folder "CrowdHuman_train01", "CrowdHuman_train02", "CrowdHuman_train03", "CrowdHuman_test", "CrowdHuman_val" in the same folder.

The dataset download link is mentioned in the website mentioned below.

[Crowd Human Dataset Website](https://www.crowdhuman.org/)

[Crowd Human Dataset Paper Link](https://arxiv.org/pdf/1805.00123.pdf)
