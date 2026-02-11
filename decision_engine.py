import os

def select_best_file(file_group):
    return max(file_group, key=lambda f: os.path.getsize(f))
