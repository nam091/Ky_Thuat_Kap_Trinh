import os
import cv2
import numpy as np
from PIL import Image
from Function_support import (
    max_bits_to_hide, 
    get_filesize, 
    bytes_in_max_file_size, 
    secret_encode,
    hash_password,
    Begin_message_print, 
    Done_message_print,
)

def Image_steganography(action: int, input_file, output_file, secret, num_lsb: int, compression_level: int):
    """
    Giải thích:
    - action: 0 là phân tích, 1 là ẩn tin, 2 là giải mã
    - input_file: đường dẫn file ảnh
    - out_put_file: đường dẫn file output
    - secret: đường dẫn file secret
    - num_lsb: số bit LSB sử dụng để ẩn tin
    - compression_level: mức độ nén để giúp giảm kích thước file
    """
    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        raise FileNotFoundError(f"[-] Error: File {input_file} not found")
    else:
        
        image_opened = Image.open(input_file, 'r')
        num_channels = len(image_opened.getbands())
        image_cv2 = cv2.imread(input_file)
        Max_byte_of_image_chosen = bytes_in_max_file_size(image_opened, num_lsb, num_channels)
    
    def Analysis():
        Begin_message_print("Analysis")
        with image_opened:
            print(f"[*] Image resolution: ({image_opened.size[0]}, {image_opened.size[1]}, {len(image_opened.getbands())})")
            print(f"[*] Sử dụng {num_lsb} LSBs, Có thể ẩn tin: {max_bits_to_hide(image_opened, num_lsb, num_channels) // 8} B")
            print(f"[*] kích thước của input file: {get_filesize(input_file)} B")
            print(f"[*] Kích thước tối đa có thể ẩn tin: {Max_byte_of_image_chosen} B")
        print("=" * 100)

    def Encode(): # Hàm Encode nhận thêm num_lsb và compression_level
        Begin_message_print("Encode")
        print(f"[*] Sử dụng {num_lsb} LSBs") # Thêm thông tin về số LSB
        print(f"[*] PNG cấp độ nén: {compression_level}") # Thêm thông tin về compression level
        print("=" * 100)

        password = input("[*] Nhập mật khẩu (tùy chọn) -- Enter để bỏ qua: ")
        hashed_password = hash_password(password)

        secret_message = secret_encode(secret)
        if len(secret_message) > Max_byte_of_image_chosen:
            raise ValueError(f"[-] Error: Tin mật quá lớn so với kích thước của ảnh\n"
                     f"[-] kích thước Maximum bytes để giấu trong ảnh: {Max_byte_of_image_chosen}\n"
                     f"[-] Kích thước Secret file: {len(secret_message)}\n"
                     f"[-] Hãy sử dụng ảnh lớn hơn hoặc giảm kích thước của secret file\n"
                     f"[-] Nếu tang số bit LSB sẽ làm tăng dung lượng ảnh có thể chứa và giảm chất lượng ảnh")
        
        if out_put_file is None:
            out_put_file = os.path.splitext(secret_message)[0] + "_encoded.png"
        try:
            encoded_image = Hide_data(secret_message, hashed_password) # Truyền num_lsb
            
            exif_data = image_opened.info.get('exif') # Copy metadata sang ảnh mới
            
            encoded_image.save(output_file, compress_level=compression_level, exif=exif_data)
            Done_message_print("Encode", output_file)
        except ValueError as e:
            print(f"[INFO] Encoding Error: {e}")
            print("=" * 100)
    
    def Hide_data(secret_message: bytes, password_hash: str):
        """
        secret_message: Dữ liệu cần giấu đã được chuyển đổi thành byte.
        num_lsb: Số lượng bit LSB để sử dụng cho việc giấu tin.
        password_hash: SHA512 hash của mật khẩu (nếu có).
        """
        pixels = np.array(image_opened) # Chuyển đổi hình ảnh thành mảng numpy
        width, height, channels = pixels.shape
        data = secret_message
        data_bits = ''.join([format(byte, '08b') for byte in data]) # Chuyển đổi dữ liệu thành một chuỗi bit
        
        padding_needed = (num_lsb - (len(data_bits) % num_lsb)) % num_lsb
        data_bits += '0' * padding_needed # Đảm bảo số lượng bit là bội số của num_lsb
        
        # Nếu có password hash, sử dụng nó để xáo trộn vị trí các pixel
        if password_hash:
            rng = np.random.default_rng(seed=int(password_hash, 16))
            pixel_indices = list(np.ndindex(height, width, channels))
            rng.shuffle(pixel_indices)
        else:
            pixel_indices = list(np.ndindex(height, width, channels))
        
        bit_index = 0 
        # Lặp qua từng pixel của ảnh
        for pixel_index in pixel_indices: 
            i, j, k = pixel_index
            if bit_index >= len(data_bits):
                break # Nếu đã giấu hết dữ liệu, thoát vòng lặp
            pixel = pixels[i, j, k] # Lấy giá trị pixel hiện tại
            pixel &= ~( (2**num_lsb - 1) ) # Xóa các bit LSB của pixel
            data_chunk = data_bits[bit_index:bit_index + num_lsb]# Lấy các bit từ dữ liệu
            data_int = int(data_chunk, 2) # Chuyển đổi các bit thành số nguyên
            pixel |= data_int # Ghi các bit vào pixel
            pixels[i, j, k] = pixel # Cập nhật giá trị pixel
            bit_index += num_lsb # Tăng chỉ số bit
        
        encoded_image = Image.fromarray(pixels)
        return encoded_image
    
    def Decode():
        Begin_message_print("Decode")
        print("=" * 100)
        password = input("[*] Nhập mật khẩu (tùy chọn) -- Enter để bỏ qua: ")
        hashed_password = hash_password(password)
        try:
            decoded_data = Extract_data(hashed_password)
            
            # Ghi dữ liệu giải mã vào file output
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(decoded_data)
                Done_message_print("Decode", output_file)
            else:
                print(decoded_data)
                Done_message_print("Decode", "terminal")
        except ValueError as e:
            print(f"[INFO] Decoding Error: {e}")
            print("=" * 100)
            
    def Extract_data(hashed_password):
        """
        Giải mã dữ liệu ẩn từ ảnh.
        """
        pixels = np.array(image_opened)
        width, height, channels = pixels.shape
        
        data_bits = ""
        extracted_data = bytearray()
        
        # Nếu có password hash, sử dụng nó để xáo trộn vị trí các pixel
        if hashed_password:
            rng = np.random.default_rng(seed=int(hashed_password, 16))
            pixel_indices = list(np.ndindex(height, width, channels))
            rng.shuffle(pixel_indices)
        else:
            pixel_indices = list(np.ndindex(height, width, channels))
        for pixel_index in pixel_indices:
            i, j, k = pixel_index
            pixel = pixels[i, j, k]
            lsb_values = pixel & (2**num_lsb - 1)  # Lấy giá trị của num_lsb bit LSB
            binary_chunk = format(lsb_values, '0' + str(num_lsb) + 'b')  # Chuyển đổi thành chuỗi bit
            data_bits += binary_chunk  # Thêm vào chuỗi bit
            
            # Chuyển đổi chuỗi bit thành byte
            while len(data_bits) >= 8:
                byte_data = data_bits[:8]
                data_bits = data_bits[8:]
                extracted_data.append(int(byte_data, 2))
                
                # Kiểm tra xem có phải là kết thúc dữ liệu không (null byte)
                if extracted_data[-1] == 0:
                    # Loại bỏ padding và null terminator
                    extracted_data = extracted_data[:-1]
                    # Tìm vị trí của null terminator
                    try:
                        null_index = extracted_data.index(0)
                        extracted_data = extracted_data[:null_index]
                    except ValueError:
                        pass
                    
                    # Chuyển đổi thành chuỗi và trả về
                    return extracted_data.decode('utf-8', errors='ignore')
        
    
    match action:
        case 0:
            Analysis()
        case 1:
            Encode()
        case 2:
            Decode()
        case _:
            print("Invalid action")
    image_opened.close()
Image_steganography(1,".\img\Original_image\org1.jpg", ".\img\Original_image\kneew.png", "Hello moi nguoi", 2, 1)