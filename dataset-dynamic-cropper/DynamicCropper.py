from .__main__ import Main, main

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
        img, bbs, label_path = grabber.get_data(img_path)  # Could raise an exception
        processed_file, out_img, out_bbs = self.crop_img(img, bbs)
        out_label = out_bbs.label()
        if processed_file:
            out_img_path = output_path + "/" + os.path.basename(img_path)
            # out_label_path = out_img_path.replace(self.image_extension, ".txt")
            pre_extension_path, extension = os.path.splitext(out_img_path.replace("\\", "/"))
            out_label_path = pre_extension_path + ".txt"
            grabber.write_data(out_img_path, out_label_path, out_img, out_label)
        return processed_file
    
    def process_directory(self, input_path, output_path = None, image_extension = "png", skip = 1):
        if output_path == None:
            output_path = input_path + "/cropped"
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        processed_files = 0
        counter = 0
        for img_path in glob.iglob(input_path + '/*' + image_extension):
            counter += 1
            if counter % self.skip == 0:
                if self.process_file(img_path, output_path):
                    processed_files += 1
        return processed_files

    def process_directory_recursively(self, input_path, output_path = None, image_extension = "png", skip = 1):
        processed_files = 0
        counter = 0
        for root_path, dir_paths, file_paths in os.walk(input_path):
            for img_path in file_paths:
                if img_path.endswith(image_extension):
                    img_path = os.path.join(root_path, img_path)
                    directory_path = os.path.dirname(img_path)
                    current_output_path = None
                    if output_path == None:
                        if not directory_path.replace("\\", "/").endswith("/cropped"):
                            current_output_path = directory_path + "/cropped"
                        else:
                            continue
                    else:
                        current_output_path = directory_path.replace(input_path, output_path)
                    counter += 1
                    if counter % self.skip == 0:
                        if not os.path.exists(current_output_path):
                            os.mkdir(current_output_path)
                        if self.process_file(img_path, current_output_path):
                            processed_files += 1
        return processed_files

    def dynamic_crop(self, input_path, output_path, image_extension="png", skip=1, recursive=False):
        total_processed_files = 0
        if recursive:
            print("Processing dataset...")
            total_processed_files = self.process_directory_recursively(input_path, output_path, image_extension, skip)
        else:
            print("Processing directory...")
            total_processed_files = self.process_directory(input_path, output_path, image_extension, skip)

        print("\nProcessed {processedCount} files.".format(processedCount = total_processed_files))
        print("All Done!")
