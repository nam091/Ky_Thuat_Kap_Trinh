import os
import io
from PIL import Image
import numpy as np
import hashlib
import webbrowser
from datetime import datetime

def save_jpeg(image, quality):
    temp_buffer = io.BytesIO()
    image.save(temp_buffer, 'JPEG', quality=quality)
    temp_buffer.seek(0)
    return Image.open(temp_buffer)

def calc_error_level(image_path, quality, scale):
    original_image = Image.open(image_path).convert('RGB')
    reduced_quality_image = save_jpeg(original_image, quality)

    original_array = np.array(original_image)
    reduced_array = np.array(reduced_quality_image)

    diff_array = np.abs(original_array - reduced_array)
    ela_array = np.uint8(np.clip(diff_array * scale, 0, 255))

    ela_image = Image.fromarray(ela_array)
    return ela_image

def calculate_hash(file_path, algorithm):
    hash_object = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        chunk_size = 4096
        while chunk := file.read(chunk_size):
            hash_object.update(chunk)
    return hash_object.hexdigest()

def create_report(quality, scale, original_path, ela_path, report_path):
    now = datetime.now().strftime("%d/%MM/%YYYY %H:%M:%S")
    md5_original = calculate_hash(original_path, 'md5')
    sha1_original = calculate_hash(original_path, 'sha1')
    md5_ela = calculate_hash(ela_path, 'md5')
    sha1_ela = calculate_hash(ela_path, 'sha1')

    try:
        with open('report_template.html', 'r', encoding='utf-8') as template_file:
            html_template = template_file.read()
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file report_template.html.")
        return

    html_content = html_template.replace('{{report_date}}', now) \
                                .replace('{{quality}}', str(quality)) \
                                .replace('{{scale}}', str(scale)) \
                                .replace('{{original_path}}', original_path) \
                                .replace('{{md5_original}}', md5_original) \
                                .replace('{{sha1_original}}', sha1_original) \
                                .replace('{{ela_path}}', ela_path) \
                                .replace('{{md5_ela}}', md5_ela) \
                                .replace('{{sha1_ela}}', sha1_ela)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Báo cáo đã được lưu tại: {report_path}")
    webbrowser.open('file://' + os.path.abspath(report_path))

if __name__ == "__main__":
    image_path = input("Nhập đường dẫn ảnh: ")
    if not os.path.exists(image_path):
        print("File ảnh không tồn tại.")
        exit()

    quality = int(input("Nhập chất lượng JPEG (0-100): "))
    scale = int(input("Nhập hệ số tỷ lệ (ví dụ: 10): "))
    generate_report_choice = input("Tạo báo cáo HTML? (yes/no): ").lower()
    generate_report = generate_report_choice == 'yes'

    ela_image = calc_error_level(image_path, quality, scale)

    ela_filename_base = "ELA_" + os.path.splitext(os.path.basename(image_path))[0]
    ela_image_path = ela_filename_base + ".jpg"
    ela_image.save(ela_image_path)
    print(f"Ảnh ELA đã được lưu tại: {ela_image_path}")
    ela_image.show()

    if generate_report:
        original_filename_base = os.path.splitext(os.path.basename(image_path))[0]
        report_path = original_filename_base + "_ELA_report.html"
        create_report(quality, scale, image_path, ela_image_path, report_path)

    print("Tiến trình ELA hoàn tất.")