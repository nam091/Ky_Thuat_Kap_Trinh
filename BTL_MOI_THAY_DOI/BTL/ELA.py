import numpy as np
import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2


def calculate_hash(file_path, hash_type='md5'):
    """Tính toán hash của file với loại hash được chỉ định (MD5 hoặc SHA-1)."""
    hash_func = hashlib.md5() if hash_type.lower() == 'md5' else hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def generate_html_report(original_path, ela_path, temp_path, quality, scale, ratio):
    """Tạo báo cáo HTML từ template."""
    # Chỉ lấy tên file của ela_path nếu cần dùng đường dẫn tương đối trong HTML
    ela_basename = os.path.basename(ela_path)
    
    # Tính toán hash
    md5_original = calculate_hash(original_path, 'md5')
    sha1_original = calculate_hash(original_path, 'sha1')
    md5_ela = calculate_hash(ela_path, 'md5')
    sha1_ela = calculate_hash(ela_path, 'sha1')
    
    # Đọc file template HTML
    with open('.\Report_ELA\\report_template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    if ratio >= 0.2:
        ratio_message = f"Ảnh có dấu hiệu đã bị chỉnh sửa với {ratio:.2%} pixel nghi ngờ"
    elif ratio < 0.2:
        ratio_message = f"Ảnh không có dấu hiệu bị chỉnh sửa với {ratio:.2%} pixel nghi ngờ"
    # Thay thế các placeholder bằng giá trị thực tế
    report_data = {
        'original_path': original_path,
        'original_name' :os.path.basename(temp_path),
        'ela_path': os.path.basename(ela_path),
        'quality': quality,
        'scale': scale,
        'md5_original': md5_original,
        'sha1_original': sha1_original,
        'md5_ela': md5_ela,
        'sha1_ela': sha1_ela,
        'ratio': ratio_message
    }
    report = template.format(**report_data)
    
    # Lưu báo cáo HTML
    output_path = '.\Report_ELA\Report_ELA.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Báo cáo HTML đã được lưu tại '{output_path}'")

def perform_ela(image_path, ela_path, temp_path, quality=90, scale=5):
    try:
        # Kiểm tra file hợp lệ
        if not os.path.exists(image_path):
            raise ValueError("File ảnh không tồn tại!")
        # if not image_path.lower().endswith(('.jpg', '.jpeg')):
        #     raise ValueError("Vui lòng chọn file JPEG!")

        # Đọc ảnh gốc
        original = cv2.imread(image_path)
        if original is None:
            raise ValueError("Không thể đọc ảnh.")

        # Lưu ảnh với chất lượng thấp h
        cv2.imwrite(temp_path, original, [cv2.IMWRITE_JPEG_QUALITY, quality])
        
        # Đọc ảnh nén
        compressed = cv2.imread(temp_path)
        
        # Tính sự khác biệt
        diff = cv2.absdiff(original, compressed)
        
        # Phóng đại sự khác biệt
        ela = cv2.convertScaleAbs(diff, alpha=scale)
        
        # Chuyển sang ảnh xám
        ela_gray = cv2.cvtColor(ela, cv2.COLOR_BGR2GRAY)
        
        # Áp dụng ngưỡng Otsu
        _, thresh = cv2.threshold(ela_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Tính tỷ lệ pixel nghi ngờ
        suspicious_pixels = np.sum(thresh == 255)
        total_pixels = thresh.size
        ratio = suspicious_pixels / total_pixels
        
        # Lưu ảnh ELA để kiểm tra
        cv2.imwrite(ela_path, ela_gray)
        
        return ratio

    except Exception as e:
        print(f"Đã xảy ra lỗi: {str(e)}")
        return None

def gui():
    def run_ela():
        image_path = filedialog.askopenfilename(title="Chọn ảnh JPEG", filetypes=[("JPEG files", "*.jpg *.jpeg *.png")])
        temp_path = '.\Report_ELA\Temp_original.jpg'
        if not image_path:
            return
        ela_path = '.\Report_ELA\ELA_result.png'
        try:
            quality = int(quality_var.get())
            scale = int(scale_var.get())
            report = report_var.get()
            
            ratio = perform_ela(image_path, ela_path, temp_path, quality, scale)
            if ratio is not None:
                # Tạo báo cáo HTML nếu được chọn
                if report:
                    generate_html_report(image_path, ela_path, temp_path,quality, scale, ratio)
            else:
                messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi thực hiện ELA.")
        except ValueError as e:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho chất lượng và hệ số phóng đại!")

    root = tk.Tk()
    root.title("Error Level Analysis Tool")
    
    tk.Label(root, text="Chất lượng JPEG (0-100):").pack(pady=5)
    quality_var = tk.StringVar(value="90")
    tk.Entry(root, textvariable=quality_var).pack()
    
    tk.Label(root, text="Hệ số phóng đại (0-50):").pack(pady=5)
    scale_var = tk.StringVar(value="5")  # Giá trị mặc định giảm xuống 5
    tk.Entry(root, textvariable=scale_var).pack()
    
    report_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="Tạo báo cáo HTML", variable=report_var).pack(pady=5)
    
    tk.Button(root, text="Mở File", command=run_ela).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    gui()