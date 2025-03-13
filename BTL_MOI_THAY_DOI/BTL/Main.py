import argparse
import os
from Metadata import Metadata_extract_image

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
            metadata = Metadata_extract_image(image_path)
            
            print("=" * 100)
            print("Metadata for {image_path}:")
            print("=" * 100)
            
            if metadata is None:
                print(f"Error: Failed to extract metadata from {image_path}")
            else:
                for key in metadata:
                    if isinstance(key, str):
                        if isinstance(metadata[key], dict):
                            print(f"{key}:")
                            for subkey in metadata[key]:
                                print(f"  {subkey}: {metadata[key][subkey]}")
                        else:
                            print(f"{key}: {metadata[key]}")