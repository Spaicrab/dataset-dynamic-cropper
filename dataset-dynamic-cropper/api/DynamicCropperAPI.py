from . import main

class DynamicCropperAPI:
    def dynamic_crop(self, input_directory, image_extension, crop_size, recursive):
        args = [input_directory, '-e', str(image_extension), '-s', str(crop_size)]
        if recursive: args.append('-r')
        main(args)