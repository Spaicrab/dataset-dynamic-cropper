from .__main__ import Main, main

class DynamicCropper:
    def __init__(self, crop_size = "640", image_extension = ".png", skip = 1):
        self.image_extension = image_extension
        self.crop_size = crop_size
        self.skip = skip

    def dynamic_crop(self, input_directory, image_extension="png", crop_size=640, skip=1, recursive=False):
        args = [input_directory, '-e', str(image_extension), '-s', str(crop_size), '-sk', str(skip)]
        if recursive: args.append('-r')
        main(args)

    def crop_img(self, img, bbs, crop_size=640):
        args = [str(None), '-s', str(crop_size)]
        cropper = Main(args)
        return cropper.crop_img(img, bbs)

    def process_file(self, img_path, output_path, crop_size=640):
        args = [str(None), '-s', str(crop_size)]
        cropper = Main(args)
        cropper.process_file(img_path, output_path)
    
    def process_directory(self, directory_path, image_extension = "png", crop_size = 640, output_path = None):
        if output_path == None:
            output_path = directory_path + "/cropped"
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        processed_files = 0
        counter = 0
        for img_path in glob.iglob(directory_path + '/*' + self.image_extension):
            counter += 1
            if counter % self.skip == 0:
                if self.process_file(img_path, output_path):
                    processed_files += 1
        return processed_files