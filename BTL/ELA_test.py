from PIL import Image
from PIL import ImageChops

def perform_ela(image_path, quality=95, scale=10):
    # Load original image and convert to RGB mode
    original = Image.open(image_path).convert('RGB')
    
    # Save with specified quality
    temp_path = 'temp.jpg'
    original.save(temp_path, 'JPEG', quality=quality)
    
    # Load compressed image and convert to RGB mode
    compressed = Image.open(temp_path).convert('RGB')
    
    # Compute difference
    diff = ImageChops.difference(original, compressed)
    
    # Convert to grayscale
    diff = diff.convert('L')
    
    # Scale the difference
    pixels = list(diff.getdata())
    scaled_pixels = [min(p * scale, 255) for p in pixels]
    scaled_diff = Image.new('L', diff.size)
    scaled_diff.putdata(scaled_pixels)
    
    # Save the ELA result
    ela_path = 'ela_result.png'
    scaled_diff.save(ela_path)
    
    return ela_path

# Sử dụng hàm
ela_result_path = perform_ela('.\img\\lenna2.jpg')
print(f"ELA result saved to {ela_result_path}")