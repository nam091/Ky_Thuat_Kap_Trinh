import os
import sys
import argparse
from Module_Stegano import Image_steganography as IMS

use_image_encode = "python ./Steganography.py -e <location of file>"
use_image_decode = "python ./Steganography.py -d <location of file>"

use_help = "python ./Steganography.py -h -----> help"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encode', action='store_true', help="For encoding")
    parser.add_argument('-d', '--decode', action='store_true', help="For decoding")
    parser.add_argument('file_path')
    args = parser.parse_args()
    image_path = args.file_path
    c = 0
    t = True
    if isinstance(image_path) and os.path.exists(image_path) and os.path.isfile(image_path):
        if args.encode and t:
            IMS(image_path, 0)
            t = False
        elif args.decode and t:
            IMS(image_path, 1)
            t = False
        else:
            c = 1
    else:
        print(f"Error with {image_path}")
        parser.print_help()
        sys.exit(0)
    if c == 1:
        parser.print_help()
        sys.exit()

if __name__ == "__main__":
    main()
