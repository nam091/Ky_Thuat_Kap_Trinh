import argparse
import os
from Location import get_location_from_image_simple as get_location
from Metadata import extract_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract metadata from images")
    parser.add_argument("file_path", help="Path to the image file")
    args = parser.parse_args()
    image_path = args.file_path
    metadata = {}
    if not os.path.exists(image_path) or not image_path:
        print(f"Error: {image_path} does not exist")
    else:
        if not os.path.isfile(image_path):
            print(f"Error: {image_path} is not a file")
        else:
            metadata["Basic_information"] = extract_image(image_path)
            metadata["Location_of_image"] = get_location(image_path)
            
            print(f"Metadata for {image_path}:")
            for key in metadata:
                if len(metadata[key]) > 0:
                    if type(metadata[key]) == dict:
                        print(f"{key}:")
                        for subkey in metadata[key]:
                            print(f"  {subkey}: {metadata[key][subkey]}")
                    else:
                        print(f"{key}: {metadata[key]}")