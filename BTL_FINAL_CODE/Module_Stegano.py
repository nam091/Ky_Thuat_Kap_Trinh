import os
import cv2
import numpy as np
from PIL import Image
import hashlib

def Image_steganography(file, n):
    # it converts data in binary format
    def data2binary(data):
        p = ''
        if type(data) == str:
            p = p.join([format(ord(i), '08b') for i in data])
        elif type(data) == bytes or type(data) == np.ndarray:
            p = [format(i, '08b') for i in data]
        return p

    # hide data in given img
    def hide_data(img, data, password_hash):
        data += "$$"  # '$$'--> secrete key
        d_index = 0
        b_data = data2binary(data)
        len_data = len(b_data)
        height, width, _ = img.shape

        # Use password hash to generate a pseudo-random number generator
        rng = np.random.default_rng(seed=int(password_hash, 16))

        # Generate a sequence of pixel indices based on the password hash
        pixel_indices = list(np.ndindex(height, width))
        rng.shuffle(pixel_indices)

        for row, col in pixel_indices:
            pix = img[row][col]
            
            if d_index < len_data:
                r = bin(pix[0])[2:].zfill(8)
                pix[0] = int(r[:-1] + b_data[d_index], 2)
                d_index += 1
            if d_index < len_data:
                g = bin(pix[1])[2:].zfill(8)
                pix[1] = int(g[:-1] + b_data[d_index], 2)
                d_index += 1
            if d_index < len_data:
                b = bin(pix[2])[2:].zfill(8)
                pix[2] = int(b[:-1] + b_data[d_index], 2)
                d_index += 1
            
            img[row][col] = pix
            
            if d_index >= len_data:
                break
        return img


    def Encode():
        print("=" * 100)
        print("[INFO] Image Steganography ENCODING")
        print("=" * 100)
        temp_file = "temp.png"
        image_cv2 = cv2.imread(file)
        img = Image.open(file, 'r')
        w, h = img.size
        data = input("[*] Enter the secret message: ")
        if len(data) == 0:
            raise ValueError("[INFO] Empty data")

        password = input("[*] Enter password: ")
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        output_file = os.path.splitext(file)[0] + "_encoded.png"
        
        enc_data = hide_data(image_cv2.copy(), data, hashed_password)
        cv2.imwrite(temp_file, enc_data)

        # Copy metadata
        img_original = Image.open(file)
        exif_data = img_original.info.get('exif')
        img_original.close()

        img1 = Image.open(temp_file, 'r')
        img1 = img1.resize((w, h), Image.Resampling.LANCZOS)

        if w != h:
            img1.save(output_file, optimize=True, quality=65, exif=exif_data)
        else:
            img1.save(output_file, exif=exif_data)

        img.close()
        img1.close()
        os.remove(temp_file)
        print("=" * 100)
        print("[INFO] ENCODING DATA Successful")
        print("[INFO] LOCATION:{}".format(output_file))
        print("=" * 100)

    def find_data(img, password_hash):
        bin_data = ""
        height, width, _ = img.shape

        rng = np.random.default_rng(seed=int(password_hash, 16))

        # Generate a sequence of pixel indices based on the password hash
        pixel_indices = list(np.ndindex(height, width))
        rng.shuffle(pixel_indices)

        for row, col in pixel_indices:
            pix = img[row][col]
            r = bin(pix[0])[2:].zfill(8)
            g = bin(pix[1])[2:].zfill(8)
            b = bin(pix[2])[2:].zfill(8)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

        all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

        readable_data = ""
        for i in all_bytes:
            readable_data += chr(int(i, 2))
            if readable_data[-2:] == "$$":
                break
        return readable_data[:-2]

    def Decode():
        print("[INFO] Image Steganography DECODING")
        print("")
        image_cv2 = cv2.imread(file)
        img = Image.open(file, 'r')

        password = input("[*] Enter password: ")
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        #random.seed(hashed_password) # Không cần seed vì không dùng random

        #pixel_order = generate_random_pixel_order(image_cv2)
        msg = find_data(image_cv2, hashed_password)
        img.close()
        print("[*] The Encoded data was: {}".format(msg))
        print("=" * 100)

    if n == 0:
        Encode()
    else:
        Decode()
