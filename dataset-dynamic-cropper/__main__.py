import argparse
from .DynamicCropper import DynamicCropper

def main(raw_args = None):
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Dynamically crops all images in a dataset.')
    parser.add_argument('INPUT_DIRECTORY', type=str, help='input directory')
    parser.add_argument('--output-dir', '-o', type=str, required=False, help='output directory - WARNING: if this is the same as INPUT_DIRECTORY, all files will be overwritten - default: INPUT_DIRECTORY/cropped')
    parser.add_argument('--image-ext', '-e', type=str, required=False, help='extension of dataset images - default: .png')
    parser.add_argument('--size', '-s', type=int, required=False, help='cropped image size - default: 640')
    parser.add_argument('--skip', type=int, required=False, help='skip - default: 1')
    parser.add_argument('--recursive', '-r', required=False, action='store_true', help='treat input directory as a dataset, recursively processing all subdirectories')
    args = parser.parse_args(raw_args)

    self.directory_path = args.INPUT_DIRECTORY
    self.recursive = args.recursive

    if not args.image_ext:
        self.image_extension = ".png"
    else:
        if args.image_ext[0] == ".": self.image_extension = args.image_ext
        else: self.image_extension = "." + args.image_ext
    
    if not args.size: self.cropped_size = 640
    else: self.cropped_size = args.size

    if not args.skip: self.skip = 1
    else: self.skip = args.skip

    if not args.output_dir:
        self.output_path = None
    else:
        self.output_path = args.output_dir
    
    dataset_cropper = DynamicCropper(self.cropped_size)
    dataset_cropper.dynamic_crop(self.directory_path, self.output_path,self.image_ext, self.skip, self.recursive)

if __name__ == '__main__':
    main()
