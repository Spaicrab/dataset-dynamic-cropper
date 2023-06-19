# Description

Dynamically crops all images in a dataset, centering the cropped area around the bounding boxes.
Images where all bounding boxes can't fit in the cropped image are ignored.

# Syntax

```
dataset-dynamic-cropper <INPUT_PATH> <OUTPUT_PATH> [-e <IMAGE_EXTENSION>] [-s <CROP_SIZE>] [--skip <SKIP>]
```

## Arguments

``` <INPUT_PATH> ``` Input directory with the images and their labels.

``` <OUTPUT_PATH> ``` Output directory that will contain all filtered images and labels.

``` [-e (--img-ext) <IMAGE_EXTENSION>] ``` The extension used by the dataset's images -  default: "jpg"

``` [-s (--size) <CROP_SIZE>] ``` The width and height size of the output cropped images - default: 640

``` [--skip <SKIP>] ``` The skip - default: 1

# Modules

- YoloDatasetGrabber
- BoundingBoxes
- Cropper
- DynamicCropper

**INPUT_DIRECTORY** is a directory path

**IMAGE_EXTENSION** is a string containing an image extension (such as ".jpg")

**CROP_SIZE** is a number smaller than the images' size

**RECURSIVE** is a boolean, True if you want to process all subdirectories, otherwise false