import os

def list_files_with_numbers(folder_path):
    files = os.listdir(folder_path)
    file_dict = {}
    for i, file_name in enumerate(files):
        file_dict[i] = os.path.join(folder_path, file_name)
        print(f"{i} is : {file_dict[i]}")
    return file_dict

def select_file_by_number(folder_path):
    files = list_files_with_numbers(folder_path)
    check_len = True
    if len(files) == 0:
        print("No files found in the folder.")
        return None
    elif len(files) == 1:
        return files
    while len(files) > 0:
        selected_file = {
        }
        choice = input("Enter the number of the file you want to select, or 'ALL' to select all files: ")
        if choice.upper() == "ALL":
            return files
        try:
            choice = int(choice)
            if 1 <= choice <= len(files):
                selected_file[choice] = files[choice]
                return selected_file
            else:
                print("Invalid file number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'ALL'.")
    
