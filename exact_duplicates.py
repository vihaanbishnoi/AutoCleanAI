import os
from hashing import get_file_hash

def find_exact_duplicates(file_list):
    size_map = {}
    hash_map = {}
    duplicates = []

    for file in file_list:
        try:
            size = os.path.getsize(file)
            size_map.setdefault(size, []).append(file)
        except:
            pass

    for files in size_map.values():
        if len(files) < 2:
            continue

        for file in files:
            file_hash = get_file_hash(file)
            if file_hash is None:
                continue
            hash_map.setdefault(file_hash, []).append(file)

    for files in hash_map.values():
        if len(files) > 1:
            duplicates.append(files)

    return duplicates
