import os
import sys
import argparse
from Module_Stegano import Image_steganography as IMS

use_image_encode = "python ./Steganography.py -e <location of file>"
use_image_decode = "python ./Steganography.py -d <location of file>"

use_help = "python ./Steganography.py -h -----> help"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--analyze', action='store_true', help="Analyze")
    parser.add_argument('-h', '--hide', action='store_true', help="To hide data in image")
    parser.add_argument('-r', '--recover', action='store_true', help="To recover data from image")
    parser.add_argument('-i', '--input', help="File input path")
    parser.add_argument('-o', '--output', help="File output path")
    parser.add_argument('-s', '--secret', help="Path to a file to hide in image")
    parser.add_argument('-n', '--number_of_bits', help="Number of bits")
    parser.add_argument('-c', '--compression', help="Compression 1 (best speed) to 9 (smallest file)")
    
    args = parser.parse_args()
    input_image_path = args.input
    check_status = True
    if os.path.exists(input_image_path) and os.path.isfile(input_image_path):
        if args.analyze and check_status:
            IMS(0, input_image_path, 0)
            check_status = False
        elif args.decode and check_status:
            IMS(input_image_path, 1)
            check_status = False
        else:
            c = 1
    else:
        print(f"Error with {input_image_path}")
        parser.print_help()
        sys.exit(0)
    if c == 1:
        parser.print_help()
        sys.exit()

if __name__ == "__main__":
    main()