import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from Select_file_in_folder import select_file_by_number as slf

def get_gps_metadata(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id in exif_data:
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'GPSInfo':
                    gps_info = {}
                    for gps_tag_id in exif_data.get(tag_id):
                        gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_info[gps_tag] = exif_data.get(tag_id).get(gps_tag_id)
                    return gps_info
        return None
    except Exception:
        return None

def decimal_coords(degrees, minutes, seconds, direction):
    decimal_degree = degrees + minutes / 60 + seconds / 3600
    if direction in ('S', 'W'):
        decimal_degree *= -1
    return decimal_degree

def get_location_from_image_simple(image_path):
    gps_metadata = get_gps_metadata(image_path)
    if not gps_metadata:
        return "Không có thông tin GPS"

    lat_info = gps_metadata.get('GPSLatitude')
    lon_info = gps_metadata.get('GPSLongitude')
    lat_dir = gps_metadata.get('GPSLatitudeRef', 'N')
    lon_dir = gps_metadata.get('GPSLongitudeRef', 'E')

    if lat_info and lon_info:
        try:
            lat = decimal_coords(*lat_info, lat_dir)
            lon = decimal_coords(*lon_info, lon_dir)

            geolocator = Nominatim(user_agent="image_location_finder")
            location = geolocator.reverse((lat, lon), language='vi', exactly_one=True)
            return location.address if location else "Không tìm thấy địa chỉ"
        except Exception:
            return "Lỗi xử lý địa điểm"
    return "Thiếu thông tin tọa độ"

if __name__ == "__main__":
    path_folder = r"img"
    selected_file = slf(path_folder)
    for item in selected_file.keys():
        image_path = selected_file[item]
        file_name = os.path.basename(image_path)
        address = get_location_from_image_simple(image_path)
        print(f"Địa chỉ từ ảnh {file_name}: {address}")