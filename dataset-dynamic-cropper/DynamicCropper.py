"""Dynamic cropping module"""

import os, glob
import imagesize
import cv2 as cv
from .YoloDatasetGrabber import YoloDatasetGrabber
from .BoundingBoxes import BoundingBoxes

class DynamicCropper:
    """Dynamic Cropper for Yolo format datasets"""
    def __init__(self, crop_size = "640"):
        self.crop_size = crop_size

    def crop_img(self, img, center_x, center_y):
        """Returns img cropped with center_x and center_y as center"""
        half_crop_w, half_crop_h = int(self.crop_size / 2), int(self.crop_size / 2)
        cropped_img = img[center_y - half_crop_h : center_y + half_crop_h,
                            center_x - half_crop_w : center_x + half_crop_w]
        return cropped_img

    def get_img_size(self, img):
        """Returns img width and height of img"""
        img_shape = img.shape
        return img_shape[1], img_shape[0]

    def borders_exceed(self, img_w, img_h, xM, xm, yM, ym) -> bool:
        """Returns True if bounding boxes' borders don't fit in a croppable area, otherwise False"""
        crop_w, crop_h = min(img_w, self.crop_size), min(img_h, self.crop_size)
        if xM - xm >= int(crop_w) or yM - ym >= int(crop_h):
            return True
        return False

    def get_crop_center(self, img_w, img_h, xM, xm, yM, ym):
        """Returns a point that's centered around the bounding boxes"""
        crop_w, crop_h = min(img_w, self.crop_size), min(img_h, self.crop_size)
        half_crop_w, half_crop_h = int(crop_w / 2), int(crop_h / 2)

        # If all bounding boxes fit into a cropped area centered
        # around the middle of the image, don't crop
        #
        # middle_x, middle_y = int(img_w / 2), int(img_h / 2)
        # centerMargines = [middle_x + half_crop_w, middle_x - half_crop_w,
        #                   middle_y + half_crop_h, middle_y - half_crop_h]
        # # fitsInMiddleMargines = True
        # for i in range(4):
        #     if i % 2 == 0:
        #         if not centerMargines[i] >= marginList[i]:
        #             fitsInMiddleMargines = False
        #     else:
        #         if not centerMargines[i] <= marginList[i]:
        #             fitsInMiddleMargines = False
        # if fitsInMiddleMargines:
        #     return middleX, middleY
        # else:

        center_x = int((xM + xm) / 2)
        center_y = int((yM + ym) / 2)

        if half_crop_w <= center_x:
            if center_x > img_w - half_crop_w:
                center_x = img_w - half_crop_w
        else:
            center_x = half_crop_w
        
        if half_crop_h <= center_y:
            if center_y > img_h - half_crop_h:
                center_y = img_h - half_crop_h
        else:
            center_y = half_crop_h
        
        return center_x, center_y

    def dynamic_crop(self, img, bbs):
        """Returns img and bbs cropped dynamically"""
        img_w, img_h = self.get_img_size(img)
        bbs.to_pixel(img_w, img_h)
        xM, xm, yM, ym = bbs.borders()
        if self.borders_exceed(img_w, img_h, xM, xm, yM, ym):
            raise Exception("The bounding boxes can't fit into the cropped area.")
        center_x, center_y = self.get_crop_center(img_w, img_h, xM, xm, yM, ym)
        cropped_img = self.crop_img(img, center_x, center_y)
        cropped_img_w, cropped_img_h = self.get_img_size(cropped_img)
        bbs.to_cropped(cropped_img_w, cropped_img_h, center_x, center_y)
        return cropped_img, bbs

    def process_file(self, img_path, output_path):
        """Takes an image and its label file and writes their dynamically cropped version to output_path"""
        grabber = YoloDatasetGrabber()
        img, bbs, label_path = grabber.get_data(img_path)
        out_img, out_bbs = self.dynamic_crop(img, bbs)
        img_name = os.path.basename(img_path)
        grabber.write_data(output_path, img_name, out_img, out_bbs)

    def process_directory(self, input_path, output_path = None, image_extension = "png", skip = 1, recursive = True):
        """Dynamically crops a dataset and writes the output to output_path"""
        print("Processing dataset...")
        filtered_files = 0
        total_processed_files = 0
        os.makedirs(output_path, exist_ok=True )
        grabber = YoloDatasetGrabber()
        for img, bbs, img_path, label_path in grabber.iget_directory_data(input_path, image_extension, recursive):
            total_processed_files += 1
            print(f"\r{img_path}", end="\x1b[1K")
            if total_processed_files % skip != 0:
                continue
            try:
                out_img, out_bbs = self.dynamic_crop(img, bbs)
            except:
                continue
            filtered_files += 1
            img_name = os.path.basename(img_path)
            grabber.write_data(output_path, img_name, out_img, out_bbs)
        print(f"\rFiltered {filtered_files} of {total_processed_files} files.")
        return total_processed_files, filtered_files
