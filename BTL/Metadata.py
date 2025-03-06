from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from File_Format import File_Format_Folder

def extract_svg(svg_path):
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

def extract_image(image_path):
    # Xác định kiểu file để dễ dàng xử lý
    try:
        file_extension = File_Format_Folder(image_path)
        if "error" in file_extension:
                print(f"Lỗi xác định kiểu file cho {file_extension['file_name']}: {file_extension['error']}")
                return None
        file_extension = file_extension['Dinh_dang']
        
        # Xử lý các kiểu file khác nhau
        if file_extension.upper() == 'SVG':
            return extract_svg(image_path)
        
        elif file_extension.upper() in ['JPG', 'JPEG', 'PNG']:
            img = Image.open(image_path)
            exif_data = img.getexif()
            metadata = {}
            
            for tagid in exif_data:
                tagname = TAGS.get(tagid, tagid)
                value = exif_data.get(tagid)
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
        else:
            return f"Unsupported file format: {file_extension}"
            
    except Exception as e:
        print(f"Error extracting metadata: {str(e)}")
        return None
