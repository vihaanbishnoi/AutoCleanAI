import os

def scan_folder(folder_path):
    file_list = []

    for root, dirs, files in os.walk(folder_path):

        # Skip quarantine folder
        if "quarantine" in root.lower():
            continue

        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(root, file)
                file_list.append(full_path)

    return file_list
