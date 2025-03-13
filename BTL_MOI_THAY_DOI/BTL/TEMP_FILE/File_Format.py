import magic as mg
import os
from Select_file_in_folder import select_file_by_number as slf

def File_Format(File_path):
    try:
        file_detail = mg.from_file(File_path)
        file_detail = file_detail.split(" ")[0]
        return {
            "Dinh_dang": file_detail
        }
    except FileNotFoundError:
        return {"error": "File không tồn tại"}
    except Exception as e:
        return {"error": f"Lỗi: {e}"}

def File_Format_Folder(File_path):
    if not File_Format:
        return {"error": "File không tồn tại"}
    result = []
    if os.path.isfile(File_path):
        try:
            File_name = os.path.basename(File_path)
            file_detail = mg.from_file(File_path).split(" ")[0]
            Result = ({
                "file_name": File_name,
                "Dinh_dang": file_detail
            })
        except Exception as e:
            Result = ({
                "file_name": File_name,
                "error": f"Lỗi: {e}"
            })
    return Result


def missing_input_file():
    Folder_path = r"img"
    selected_file = slf(Folder_path)

    for item in selected_file.keys():
        Result = File_Format_Folder(selected_file[item])

        if "error" in Result:
            print(f"Lỗi: {Result['error']}")
        else:
            for file_info in Result:
                if "error" in file_info:
                    print(f"Lỗi xác định kiểu file cho {file_info['file_name']}: {file_info['error']}")
                else:
                    print(f"Định dạng file {file_info['file_name']} là: {file_info['Dinh_dang']}")


if __name__ == "__main__":
    result = File_Format_Folder("./img/org1.jpg")
    print(result["Dinh_dang"])