"""Yolo format dataset grabber util"""

import os, glob
import cv2 as cv
from .BoundingBoxes import BoundingBoxes

class YoloDatasetGrabber:
    """Grabber util for Yolo format"""
    def get_data(self, img_path):
        """Read data from img file
        Returns opencv tensor image, BoundingBoxes bbs, label_path"""
        img = cv.imread(img_path)
        pre_extension_path, extension = os.path.splitext(img_path.replace("\\", "/"))
        label_path = pre_extension_path + ".txt"
        if not os.path.exists(label_path):
            raise Exception(img_path + " doesn't have a label.")
        with open(label_path, 'r') as label:
            try: bbs = BoundingBoxes(label)
            except: raise Exception(label_path + " uses an incorrect format.")
            return img, bbs, label_path
    
    def write_data(self, output_path, img_name, img, bbs):
        """Write data to output path"""
        label = bbs.label()
        img_path = output_path + "/" + img_name
        pre_extension_path, extension = os.path.splitext(img_path.replace("\\", "/"))
        label_path = pre_extension_path + ".txt"
        cv.imwrite(img_path, img)
        with open(label_path , 'w') as f:
            f.write(label)
    
    def iget_directory_data(self, directory_path, img_extension="jpg", recursive=False):
        """Read data of all img files in the directory and its subdirectories.
        Iterates over img, bbs, img_path, label_path"""
        file_condition = directory_path
        if recursive:
            file_condition += '/**/*.' + img_extension
        else:
            file_condition += '/*.' + img_extension
        for img_path in glob.iglob(file_condition, recursive=recursive):
            try:
                img, bbs, label_path = self.get_data(img_path)
                yield img, bbs, img_path, label_path
            except:
                pass

    def get_directory_data(self, directory_path, img_extension="jpg", recursive=False):
        """Read data of all img files in the directory and its subdirectories.
        Returns a list of tuples with img, bbs, img_path, label_path"""
        return list(self.iget_directory_data(directory_path, img_extension, recursive))
