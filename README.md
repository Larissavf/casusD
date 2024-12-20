# Dataset Preparation for Object Detection in YOLO Format

This script facilitates the creation of a dataset directory structure, processes bounding box annotations, and organizes training and validation datasets for object detection models in YOLO format.

## Features
- **Dataset Directory Structure**: Automatically creates a dataset folder with subdirectories for training and validation images and labels.
- **Annotation Conversion**: Converts bounding box annotations to YOLO format with normalized coordinates.
- **Random File Selection**: Randomly selects files for training and validation datasets.
- **Image Copying**: Copies the selected images and their corresponding labels to the appropriate dataset directories.

## Setup
- Make sure you change mypath in the file Opdracht_3.py to the correct path.

## Editing the parameters
To edit the parameters of the trainingdata you can edit the following items.
- Line 124 edit the num_files
- Line 125 edit the num_files
- in the model.train in 3_test.py. You can edit the epochs to change how many it will execute

## Prerequisites
- Python 3.x
- Required Python libraries:
  - `os`
  - `Pillow` (PIL)
  - `random`
  - `shutil`

Install the required libraries using pip if they are not already installed:
```bash
pip install pillow
