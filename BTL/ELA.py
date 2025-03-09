from PIL import Image, ImageChops

def calculate_ela(image_path, scale=10):
    """
    Tính toán ELA cho ảnh.

    Args:
        image_path (str): Đường dẫn đến file ảnh.
        scale (int): Hệ số tỷ lệ JPEG.

    Returns:
        Image.Image: Ảnh ELA.
    """
    try:
        original = Image.open(image_path).convert('RGB')
        resaved = original.copy()
        resaved.save("resaved.jpg", "JPEG", quality=scale)
        resaved = Image.open("resaved.jpg")

        ela = ImageChops.difference(original, resaved)
        ela = ela.convert('L')  # Chuyển đổi sang thang độ xám
        
        # Tăng cường độ sáng để dễ nhìn
        max_diff = 0
        for x in range(ela.size[0]):
            for y in range(ela.size[1]):
                max_diff = max(max_diff, ela.getpixel((x, y)))
        
        if max_diff > 0:
            scale_factor = 255.0 / max_diff
            for x in range(ela.size[0]):
                for y in range(ela.size[1]):
                    ela.putpixel((x, y), int(ela.getpixel((x, y)) * scale_factor))
        
        return ela

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file ảnh tại '{image_path}'")
        return None
    except Exception as e:
        print(f"Lỗi: Có lỗi xảy ra trong quá trình xử lý ảnh: {e}")
        return None

if __name__ == '__main__':
    image_path = input("Nhập đường dẫn đến file ảnh: ")
    ela_image = calculate_ela(image_path)

    if ela_image:
        ela_image.show()  # Hiển thị ảnh ELA
        ela_image.save("ela_output.png") # Lưu ảnh ELA (tùy chọn)