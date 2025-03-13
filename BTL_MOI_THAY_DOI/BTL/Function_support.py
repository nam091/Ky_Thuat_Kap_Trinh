import os
import sys
from math import ceil
from PIL import Image
from typing import Union
import hashlib


def roundup(x: float, base: int = 1) -> int: # Hàm làm tròn lên
    return int(ceil(x / base)) * base

def max_bits_to_hide(image: Image, num_lsb: int, num_channels: int) -> int:
    return image.size[0] * image.size[1] * num_channels * num_lsb

def get_filesize(file_path: str) -> int:
    return os.path.getsize(file_path)

def bytes_in_max_file_size(image: Image, num_lsb: int, num_channels: int) -> int:
    return roundup(max_bits_to_hide(image, num_lsb, num_channels) / 8)
    
def secret_encode(secret: Union[str, bytes]):
    if secret is None:
        secret_message = input("[*] Nhập Tin nhắn mật (Không được bỏ trống) -- Đường dẫn hoặc đoạn text trực tiếp: ")
        if not secret_message:
                print("[ERROR] Tin nhắn mật không được bỏ trống")
                sys.exit(1)
        if isinstance(secret_message, str):
            secret_message = secret_message.encode("utf-8")
    else:
        if isinstance(secret, str) and os.path.exists(secret) and os.path.isfile(secret):
            with open(secret, "rb") as input_file:
                secret_message = input_file.read()
        elif isinstance(secret, bytes):
            secret_message = secret
        else:
            print("[ERROR] Tin nhắn mật không hợp lệ")
            sys.exit(1)
    # Chuyển đổi kích thước tin nhắn thành biểu diễn byte
    message_size = len(secret_message)
    size_bytes = message_size.to_bytes(4, byteorder='big')  # Sử dụng 4 byte để biểu diễn kích thước
    return size_bytes + secret_message

def hash_password(password):
    if password:
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
    else:
        hashed_password = ""
    return hashed_password

def Done_message_print(action: str, output_file_path: str):
    print("=" * 100)
    match action:
        case "Analysis":
            print("[INFO] ANALYSIS DATA Successful")
        case "Encode":
            print("[INFO] ENCODING DATA Successful")
        case "Decode":
            print("[INFO] DECODING DATA Successful")
        case _:
            print("[INFO] UNKNOWN ACTION")
    print("[INFO] LOCATION:{}".format(output_file_path))
    print("=" * 100)
    
def Begin_message_print(action: str):
    print("=" * 100)
    match action:
        case "Analysis":
            print("[INFO] Image Analysis")
        case "Encode":
            print("[INFO] Image Steganography HIDING")
        case "Decode":
            print("[INFO] Image Steganography RECOVERING")
        case _:
            print("[INFO] UNKNOWN ACTION")
    print("=" * 100)