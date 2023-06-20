# Description
Dynamically crops all images in a dataset, centering the cropped area around the bounding boxes.
Images with bounding boxes that don't fit in a croppable area are ignored.

The modules BoundingBoxes and YoloDatasetGrabber are utils used for handling datasets.

# Syntax
```
dataset-dynamic-cropper <INPUT_PATH> <OUTPUT_PATH> [-e <IMAGE_EXTENSION>] [-s <CROP_SIZE>] [--skip <SKIP>]
```

## Arguments
``` <INPUT_PATH> ``` Input directory with the images and their labels.

``` <OUTPUT_PATH> ``` Output directory that will contain all filtered images and labels.

``` [-e (--img-ext) <IMAGE_EXTENSION>] ``` The extension used by the dataset's images -  default: "jpg"

``` [-s (--size) <CROP_SIZE>] ``` The width and height size of the output cropped images - default: 640

``` [--skip <SKIP>] ``` Image skip interval - default: 1 (no skipping)

# Modules
- DynamicCropper: calculates bounding boxes' center and applies cropping on image
- BoundingBoxes: represents in a class all bounding boxes in a label file, with methods
- YoloDatasetGrabber: grabs (and writes to output) the images and their associated labels in a dataset

## DynamicCropper
### Usage
```
cropper = DynamicCropper(crop_size)
cropper.dynamic_crop(input_path, output_path, [image_extension], [skip], [recursive])
```

## BoundingBoxes
### Usage


## YoloDatasetGrabber
### Usage

