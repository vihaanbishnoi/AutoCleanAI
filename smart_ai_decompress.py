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

print("Detected OS:", platform.system())
print("User Home:", HOME)
print("Watching Folders:")
for f in WATCH_FOLDERS:
    print(" -", f)


# =========================
# DECOMPRESSION
# =========================
def decompress_file(file_path):

    print(f"\n🔓 Auto Decompressing: {file_path}")

    with open(file_path, "rb") as f:
        data = f.read()

    if file_path.endswith(".br"):
        original = brotli.decompress(data)
        out_file = file_path.replace(".br", "")

    elif file_path.endswith(".zlib"):
        original = zlib.decompress(data)
        out_file = file_path.replace(".zlib", "")

    elif file_path.endswith(".xz"):
        original = lzma.decompress(data)
        out_file = file_path.replace(".xz", "")

    else:
        return None

    with open(out_file, "wb") as f:
        f.write(original)

    print("✅ Restored:", out_file)
    return out_file


# =========================
# OPEN FILE USING OS DEFAULT APP
# =========================
def open_file(file_path):

    os_name = platform.system()

    print("📂 Opening using OS default app...")

    if os_name == "Darwin":      # macOS
        subprocess.run(["open", file_path])

    elif os_name == "Windows":
        os.startfile(file_path)

    elif os_name == "Linux":
        subprocess.run(["xdg-open", file_path])


# =========================
# WATCHDOG HANDLER
# =========================
class SmartHandler(FileSystemEventHandler):

    def on_modified(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        if file_path.endswith((".br", ".zlib", ".xz")):
            print("\n👀 Access detected:", file_path)

            restored = decompress_file(file_path)

            if restored:
                open_file(restored)


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    print("\n🧠 SMART AUTO DECOMPRESS SERVICE STARTED")

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