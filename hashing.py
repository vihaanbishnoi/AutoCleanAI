import hashlib

def get_file_hash(file_path):
    hasher = hashlib.sha256()

    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None
