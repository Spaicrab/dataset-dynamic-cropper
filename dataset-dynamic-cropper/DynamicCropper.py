import os, glob
import imagesize
import cv2 as cv
from .YoloDatasetGrabber import YoloDatasetGrabber
from .BoundingBoxes import BoundingBoxes

class DynamicCropper:
    def __init__(self, crop_size = "640"):
        self.crop_size = crop_size

    def crop_img(self, img, crop_w, crop_h, center_x, center_y):
        half_crop_w, half_crop_h = int(crop_w / 2), int(crop_h / 2)
        cropped_img = img[center_y - half_crop_h : center_y + half_crop_h,
                            center_x - half_crop_w : center_x + half_crop_w]
        return cropped_img

    def get_img_size(self, img):
        img_shape = img.shape
        return img_shape[1], img_shape[0]

    def borders_exceed(self, crop_w, crop_h, xM, xm, yM, ym):
        if xM - xm >= int(crop_w) or yM - ym >= int(crop_h):
            return True
        return False

    def get_crop_center(self, img_w, img_h, crop_w, crop_h, xM, xm, yM, ym):
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

    def crop(self, img, bbs):
        img_w, img_h = self.get_img_size(img)
        crop_w, crop_h = min(img_w, self.crop_size), min(img_h, self.crop_size)
        bbs.to_pixel(img_w, img_h)
        xM, xm, yM, ym = bbs.borders()
        if self.borders_exceed(crop_w, crop_h, xM, xm, yM, ym):
            raise Exception("The bounding boxes can't fit into the cropped area.")
        center_x, center_y = self.get_crop_center(img_w, img_h, crop_w, crop_h, xM, xm, yM, ym)
        cropped_img = self.crop_img(img, crop_w, crop_h, center_x, center_y)
        # cropped_img_shape = cropped_img.shape
        # bbs.to_cropped(cropped_img_shape[1], cropped_img_shape[0], center_x, center_y)
        bbs.to_cropped(crop_w, crop_h, center_x, center_y)
        return cropped_img, bbs

    def process_file(self, img_path, output_path):
        grabber = YoloDatasetGrabber()
        img, bbs, label_path = grabber.get_data(img_path)
        out_img, out_bbs = self.crop(img, bbs)
        out_label = out_bbs.label()
        out_img_path = output_path + "/" + os.path.basename(img_path)
        pre_extension_path, extension = os.path.splitext(out_img_path.replace("\\", "/"))
        out_label_path = pre_extension_path + ".txt"
        grabber.write_data(out_img_path, out_label_path, out_img, out_label)

    def process_directory(self, input_path, output_path = None, image_extension = "png", skip = 1, recursive = True):
        os.makedirs(output_path, exist_ok=True )
        filtered_files = 0
        total_processed_files = 0
        grabber = YoloDatasetGrabber()
        for img, bbs, img_path, label_path in grabber.iget_directory_data(input_path, image_extension, recursive):
            total_processed_files += 1
            print(f"\r{img_path}", end="\x1b[1K")
            if total_processed_files % skip != 0:
                continue
            try:
                out_img, out_bbs = self.crop(img, bbs)
            except:
                continue
            filtered_files += 1
            out_label = out_bbs.label()
            out_img_path = output_path + "/" + os.path.basename(img_path)
            pre_extension_path, extension = os.path.splitext(out_img_path.replace("\\", "/"))
            out_label_path = pre_extension_path + ".txt"
            grabber.write_data(out_img_path, out_label_path, out_img, out_label)
        return total_processed_files, filtered_files

    def dynamic_crop(self, input_path, output_path, image_extension = "png", skip = 1, recursive = True):
        filtered_files = 0
        print("Processing dataset...")
        total_processed_files, filtered_files = self.process_directory(input_path, output_path, image_extension, skip, recursive)
        print(f"\rFiltered {filtered_files} of {total_processed_files} files.")
