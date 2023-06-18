# Description

Dynamically crops all images in a dataset.
Images where all bounding boxes can't fit in the cropped image are scrapped.
Output is automatically put into a "cropped" directory created inside of the processed directory.

# Syntax

```
dataset-dynamic-cropper <INPUT_DIRECTORY> [-e <IMAGE_EXTENSION>] [-s <CROP_SIZE>] [-r]
```

## Arguments

```<INPUT_DIRECTORY>``` Input directory with the images and their labels.

``` [-e (--img-ext) <IMAGE_EXTENSION>] ``` The extension used by the dataset's images -  default: ".png"

``` [-s (--size) <CROP_SIZE>] ``` The width and height size of the output cropped images - default: "640"

``` [-r (--recursive)] ``` Enables recursion throughout the INPUT_DIRECTORY's subdirectories.

# API Usage
```
from api.DynamicCropperAPI import DynamicCropperAPI

api = DynamicCropperAPI()
api.dynamic_crop(INPUT_DIRECTORY, IMAGE_EXTENSION, CROP_SIZE, RESURSIVE)
```

**INPUT_DIRECTORY** is a directory path

**IMAGE_EXTENSION** is a string containing an image extension (such as ".jpg")

**CROP_SIZE** is a number smaller than the images' size

**RECURSIVE** is a boolean, True if you want to process all subdirectories, otherwise false