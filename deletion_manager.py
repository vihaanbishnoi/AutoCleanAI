import os
import shutil
from datetime import datetime

def move_to_quarantine(file_path):
    quarantine_folder = "quarantine"
    os.makedirs(quarantine_folder, exist_ok=True)

    filename = os.path.basename(file_path)
    destination = os.path.join(quarantine_folder, filename)

    shutil.move(file_path, destination)

    with open("logs/deletion_log.txt", "a") as log:
        log.write(f"{datetime.now()} - Moved: {file_path} -> {destination}\n")
