import os, glob
import cv2 as cv
from .BoundingBoxes import BoundingBoxes

class YoloDatasetGrabber:
    def get_data(self, img_path):
        img = cv.imread(img_path)
        pre_extension_path, extension = os.path.splitext(img_path.replace("\\", "/"))
        label_path = pre_extension_path + ".txt"
        if not os.path.exists(label_path):
            raise Exception(img_path + " doesn't have a label.")
        with open(os.path.join(os.getcwd(), label_path), 'r') as label:
            try: bbs = BoundingBoxes(label)
            except: raise Exception(label_path + " uses an incorrect format.")
            return img, bbs, label_path
    
    def write_data(self, img_path, label_path, img, label):
        cv.imwrite(img_path, img)
        with open(label_path , 'w') as f:
            f.write(label)
    
    def iget_directory_data(self, directory_path, image_extension):
        for img_path in glob.iglob(directory_path + '/*.' + image_extension):
            try:
                img, bbs, label_path = self.get_data(img_path)
                yield img, bbs, label_path
            except:
                pass

    def get_directory_data(self, directory_path, image_extension):
        retList = []
        for out_tuple in self.iget_directory_data(directory_path, image_extension):
            retList.append(out_tuple)
        return retList
