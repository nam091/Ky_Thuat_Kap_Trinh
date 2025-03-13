#!/usr/bin/env python3
import struct

def read_bmp_header(filename):
    with open(filename, 'rb') as f:
        # Đọc 14 byte đầu tiên (BITMAPFILEHEADER)
        file_header = f.read(14)
        
        # Giải mã BITMAPFILEHEADER
        # Format: '<2sIHHI' có nghĩa là:
        # - '<': little-endian
        # - '2s': 2 byte cho signature (kiểu string)
        # - 'I': 4 byte cho file size (kiểu unsigned int)
        # - 'H': 2 byte cho reserved1 (kiểu unsigned short)
        # - 'H': 2 byte cho reserved2 (kiểu unsigned short)
        # - 'I': 4 byte cho offset to pixel array (kiểu unsigned int)
        signature, file_size, reserved1, reserved2, offset_pixels = struct.unpack('<2sIHHI', file_header)
        
        # Đọc 40 byte tiếp theo (BITMAPINFOHEADER)
        info_header = f.read(40)
        
        # Giải mã BITMAPINFOHEADER
        # Format: '<IiiHHIIiiII' có nghĩa là:
        # - '<': little-endian
        # - 'I': 4 byte cho header size (kiểu unsigned int)
        # - 'i': 4 byte cho width (kiểu int)
        # - 'i': 4 byte cho height (kiểu int)
        # - 'H': 2 byte cho planes (kiểu unsigned short)
        # - 'H': 2 byte cho bit count (kiểu unsigned short)
        # - 'I': 4 byte cho compression (kiểu unsigned int)
        # - 'I': 4 byte cho image size (kiểu unsigned int)
        # - 'i': 4 byte cho x pixels per meter (kiểu int)
        # - 'i': 4 byte cho y pixels per meter (kiểu int)
        # - 'I': 4 byte cho colors used (kiểu unsigned int)
        # - 'I': 4 byte cho important colors (kiểu unsigned int)
        header_size, width, height, planes, bit_count, compression, image_size, x_pixels_per_meter, y_pixels_per_meter, colors_used, important_colors = struct.unpack('<IiiHHIIiiII', info_header)
        
        return {
            'signature': signature,
            'file_size': file_size,
            'reserved1': reserved1,
            'reserved2': reserved2,
            'offset_pixels': offset_pixels,
            'header_size': header_size,
            'width': width,
            'height': height,
            'planes': planes,
            'bit_count': bit_count,
            'compression': compression,
            'image_size': image_size,
            'x_pixels_per_meter': x_pixels_per_meter,
            'y_pixels_per_meter': y_pixels_per_meter,
            'colors_used': colors_used,
            'important_colors': important_colors
        }

# Sử dụng hàm để đọc header của file ảnh BMP
filename = 'output.jpg'
header = read_bmp_header(filename)
print(header)
