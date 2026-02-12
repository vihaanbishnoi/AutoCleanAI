# smart_ai_decompress.py
import os
import time
import brotli
import zlib
import lzma
import subprocess
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =========================
# AUTO DETECT USER PATH
# =========================
HOME = os.path.expanduser("~")
WATCH_FOLDERS = [
    os.path.join(HOME, "Downloads"),
    os.path.join(HOME, "Documents"),
    os.path.join(HOME, "Desktop")
]

# =========================
# DECOMPRESSION FUNCTION
# =========================
def decompress_file(file_path):
    """Decompress a file and return decompressed file path"""
    try:
        if file_path.endswith(".br"):
            with open(file_path, "rb") as f:
                data = brotli.decompress(f.read())
            out_file = file_path.replace(".br", "")

        elif file_path.endswith(".zlib"):
            with open(file_path, "rb") as f:
                data = zlib.decompress(f.read())
            out_file = file_path.replace(".zlib", "")

        elif file_path.endswith(".xz"):
            with open(file_path, "rb") as f:
                data = lzma.decompress(f.read())
            out_file = file_path.replace(".xz", "")

        else:
            return None

        with open(out_file, "wb") as f:
            f.write(data)

        return out_file

    except Exception as e:
        print("Decompression error:", e)
        return None

# =========================
# OPEN FILE USING OS DEFAULT APP
# =========================
def open_file(file_path):
    os_name = platform.system()
    try:
        if os_name == "Darwin":      # macOS
            subprocess.run(["open", file_path])
        elif os_name == "Windows":
            os.startfile(file_path)
        elif os_name == "Linux":
            subprocess.run(["xdg-open", file_path])
    except Exception as e:
        print("Open file error:", e)

# =========================
# WATCHDOG HANDLER
# =========================
class SmartHandler(FileSystemEventHandler):
    def __init__(self, tracker=None):
        self.tracker = tracker

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".br", ".zlib", ".xz")):
            restored = decompress_file(event.src_path)
            if restored:
                open_file(restored)
                if self.tracker:
                    self.tracker.add_decompressed(restored)

# =========================
# MAIN (standalone mode)
# =========================
if __name__ == "__main__":
    print("SMART AUTO DECOMPRESS SERVICE STARTED")
    observer = Observer()
    for folder in WATCH_FOLDERS:
        if os.path.exists(folder):
            observer.schedule(SmartHandler(), folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()