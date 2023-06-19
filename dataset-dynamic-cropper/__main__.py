import argparse

from .DynamicCropper import DynamicCropper


def main(raw_args=None):
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description="Dynamically crops all images in a dataset."
    )
    parser.add_argument("INPUT_DIRECTORY", type=str, help="input directory")
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        type=str,
        required=False,
        help="output directory - WARNING: if this is the same as INPUT_DIRECTORY, all files will be overwritten - default: INPUT_DIRECTORY/cropped",
    )
    parser.add_argument(
        "--image-ext",
        "-e",
        default=".jpg",
        type=str,
        required=False,
        help="extension of dataset images - default: .jpg",
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
        "--skip", type=int, default=1, required=False, help="skip - default: 1"
    )
    args = parser.parse_args(raw_args)

    if args.image_ext[0] != ".":
        args.image_ext = "." + args.image_ext

    dataset_cropper = DynamicCropper(args.size)
    dataset_cropper.dynamic_crop(
        args.INPUT_DIRECTORY, args.output_dir, args.image_ext, args.skip
    )


if __name__ == "__main__":
    main()
