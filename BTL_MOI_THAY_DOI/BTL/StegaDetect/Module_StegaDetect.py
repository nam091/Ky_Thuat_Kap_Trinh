try:
    from PIL import Image, ImageChops
    import numpy as np
    import os

except ImportError as e:
    print(f"Error importing required libraries: {e}. Please make sure you have Pillow and numpy installed.")
    exit()

def compare_images_using_diff(image_path1, image_path2):
    try:
        image1 = Image.open(image_path1).convert('RGB')
        image2 = Image.open(image_path2).convert('RGB')
        

        
        diff = ImageChops.difference(image1, image2)

        if diff.getbbox() is None:
            print("Ảnh giống nhau hoàn toàn")
            return 100.0

        image1_array = np.array(image1)
        image2_array = np.array(image2)

        diff_array = np.abs(image1_array - image2_array)

        total_pixels = image1_array.size
        different_pixels = np.count_nonzero(diff_array)

        similarity_percentage = 100.0 * (1.0 - (different_pixels / total_pixels))

        similarity_percentage = max(0.0, min(100.0, similarity_percentage))
        save_path1 = ".\Image_Output\RGB_converted_image1.png"
        save_path2 = ".\Image_Output\RGB_converted_image2.png"
        
        image1.save(save_path1)
        image2.save(save_path2)
        print(f"Tỉ lệ phần trăm trùng khớp (dựa trên sự khác biệt pixel): {similarity_percentage:.2f}%")
        return similarity_percentage

    except FileNotFoundError:
        print("Error: One or both images not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    image_path1 = "org1.jpg"
    image_path2 = "New.png"

    if not os.path.exists(image_path1):
        Image.new('RGB', (100, 100), color = 'red').save(image_path1)
    if not os.path.exists(image_path2):
        Image.new('RGB', (100, 100), color = 'blue').save(image_path2)

    similarity_percentage = compare_images_using_diff(image_path1, image_path2)