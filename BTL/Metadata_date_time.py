from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from Select_file_in_folder import select_file_by_number as slf

def extract_svg_metadata(svg_path):
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        
        metadata = {
            'Filename': os.path.basename(svg_path),
            'File Type': 'SVG',
            'Creation DateTime': datetime.fromtimestamp(os.path.getctime(svg_path)).strftime('%Y-%m-%d %H:%M:%S'),
            'Width': root.get('width'),
            'Height': root.get('height'),
            'ViewBox': root.get('viewBox')
        }
        
        return metadata
        
    except Exception as e:
        print(f"Error extracting SVG metadata: {str(e)}")
        return None

def extract_image_metadata(image_path):
    if image_path.lower().endswith('.svg'):
        return extract_svg_metadata(image_path)
    try:
        img = Image.open(image_path)
        exifdata = img.getexif()
        metadata = {}
        for tagid in exifdata:
            tagname = TAGS.get(tagid, tagid)
            value = exifdata.get(tagid)
            if isinstance(value, bytes):
                try:
                    value = value.decode()
                except:
                    value = f"Binary data of length {len(value)}"
            metadata[tagname] = value
        metadata['Filename'] = os.path.basename(image_path)
        metadata['File Type'] = image_path.split('.')[-1].upper()
        metadata['Creation DateTime'] = datetime.fromtimestamp(os.path.getctime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {str(e)}")
        return None

def main():
    image_paths = slf(r"img")
    for item in image_paths.keys():
        image_path = image_paths[item]
        metadata = extract_image_metadata(image_path)
        file_name = os.path.basename(image_path)
        if metadata:
            print(f"__________ {file_name} __________")
            for key, value in metadata.items():
                print(f"{key}: {value}")
        else:
            print(f"No metadata found for {image_path}")

if __name__ == "__main__":
    main()