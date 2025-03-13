import binascii

# Đường dẫn đến file ảnh
file_path = 'output_encoded.png'

# Đọc dữ liệu nhị phân từ file ảnh
with open(file_path, 'rb') as f:
    binary_data = f.read()

# Chuyển đổi dữ liệu nhị phân sang hex string
hex_string = binascii.hexlify(binary_data).decode('utf-8')

print(f"Hex String (first 100 characters): {hex_string[:100]}...")

# Chuyển đổi hex string trở lại dữ liệu nhị phân
binary_data_back = binascii.unhexlify(hex_string)

# Ghi dữ liệu nhị phân trở lại file (kiểm tra tính chính xác)
output_file_path = 'decodedd.txt'
with open(output_file_path, 'wb') as f:
    f.write(binary_data_back)

print(f"Dữ liệu đã được chuyển đổi và ghi lại vào file '{output_file_path}'")
