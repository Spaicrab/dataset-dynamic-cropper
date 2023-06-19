import os, glob
import imagesize
import cv2 as cv
from .YoloDatasetGrabber import YoloDatasetGrabber
from .BoundingBoxes import BoundingBoxes
from .Cropper import Cropper

class DynamicCropper:
    def __init__(self, crop_size = "640"):
        self.crop_size = crop_size

    def crop_img(self, img, bbs):
        img_shape = img.shape
        img_w, img_h = img_shape[1], img_shape[0]
        cropper = Cropper(img_w, img_h, self.crop_size, self.crop_size)
        bbs.to_pixel(img_w, img_h)
        xM, xm, yM, ym = cropper.get_borders(bbs)
        borders_exceed = not cropper.check(xM, xm, yM, ym)
        if borders_exceed:
            raise Exception("All bounding boxes don't fit into the cropped area.")
        center_x, center_y = cropper.get_crop_center(img_w, img_h, xM, xm, yM, ym)
        cropped_img = cropper.crop(img, center_x, center_y, img_w, img_h)
        cropped_img_shape = cropped_img.shape
        bbs.to_cropped(cropped_img_shape[1], cropped_img_shape[0], center_x, center_y)
        return cropped_img, bbs

    def process_file(self, img_path, output_path):
        print(f"\r{img_path}", end="")
        grabber = YoloDatasetGrabber()
        img, bbs, label_path = grabber.get_data(img_path)
        out_img, out_bbs = self.crop_img(img, bbs)
        out_label = out_bbs.label()
        out_img_path = output_path + "/" + os.path.basename(img_path)
        pre_extension_path, extension = os.path.splitext(out_img_path.replace("\\", "/"))
        out_label_path = pre_extension_path + ".txt"
        grabber.write_data(out_img_path, out_label_path, out_img, out_label)
    
    # def process_directory(self, input_path, output_path = None, image_extension = "png", skip = 1):
    #     if output_path == None:
    #         output_path = input_path + "/cropped"
    #     os.makedirs(output_path, exist_ok=True)
    #     processed_files = 0
    #     counter = 0
    #     for img_path in glob.iglob(input_path + '/*' + image_extension):
    #         counter += 1
    #         if counter % skip == 0:
    #             try:
    #                 self.process_file(img_path, output_path)
    #             except:
    #                 continue
    #             processed_files += 1
    #     return processed_files

    # def process_directory(self, input_path, output_path = None, image_extension = "png", skip = 1):
    #     os.makedirs(output_path, exist_ok=True )
    #     filtered_files = 0
    #     total_processed_files = 0
    #     for root_path, dir_paths, file_paths in os.walk(input_path):
    #         for img_path in file_paths:
    #             if img_path.endswith(image_extension):
    #                 img_path = os.path.join(root_path, img_path)
    #                 total_processed_files += 1
    #                 if total_processed_files % skip == 0:
    #                     try:
    #                         self.process_file(img_path, output_path)
    #                     except:
    #                         continue
    #                     filtered_files += 1
    #     return total_processed_files, filtered_files

    def process_directory(self, input_path, output_path = None, image_extension = "png", skip = 1):
        os.makedirs(output_path, exist_ok=True )
        filtered_files = 0
        total_processed_files = 0
        grabber = YoloDatasetGrabber()
        for img, bbs, img_path, label_path in grabber.iget_directory_data(input_path, image_extension, True):
            total_processed_files += 1
            if total_processed_files % skip != 0:
                continue
            try:
                out_img, out_bbs = self.crop_img(img, bbs)
            except:
                continue
            filtered_files += 1
            out_label = out_bbs.label()
            out_img_path = output_path + "/" + os.path.basename(img_path)
            pre_extension_path, extension = os.path.splitext(out_img_path.replace("\\", "/"))
            out_label_path = pre_extension_path + ".txt"
            grabber.write_data(out_img_path, out_label_path, out_img, out_label)
        return total_processed_files, filtered_files

    def dynamic_crop(self, input_path, output_path, image_extension = "png", skip = 1):
        filtered_files = 0
        print("Processing dataset...")
        total_processed_files, filtered_files = self.process_directory(input_path, output_path, image_extension, skip)
        print(f"\rFiltered {filtered_files} of {total_processed_files} files.")
