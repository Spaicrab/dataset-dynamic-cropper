import argparse

from .DynamicCropper import DynamicCropper

def main():
    parser = argparse.ArgumentParser(
        description="Dynamically crops all images in a dataset."
    )
    parser.add_argument("INPUT_PATH", type=str, help="input directory")
    parser.add_argument("OUTPUT_PATH", type=str, help="output directory - WARNING: if this is the same as INPUT_DIRECTORY, all files will be overwritten")
    parser.add_argument(
        "--image-ext",
        "-e",
        type=str,
        default="jpg",
        required=False,
        help="extension of dataset images - default: jpg",
    )
    parser.add_argument(
        "--size",
        "-s",
        type=int,
        default=640,
        required=False,
        help="cropped image size - default: 640",
    )
    parser.add_argument(
        "--skip", type=int, default=1, required=False, help="Image skip interval - default: 1 (no skipping)"
    )
    args = parser.parse_args()

    if args.image_ext[0] == ".":
        args.image_ext = args.image_ext[1:]

    dataset_cropper = DynamicCropper(args.size)
    dataset_cropper.dynamic_crop(
        args.INPUT_PATH, args.OUTPUT_PATH, args.image_ext, args.skip
    )

if __name__ == "__main__":
    main()
