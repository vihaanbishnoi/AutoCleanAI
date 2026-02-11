import os
import time
import joblib
import brotli
import zlib
import lzma
import math
from collections import Counter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =================================
# ASK USER OS + USERNAME
# =================================
print("=================================")
print("Universal AI Compression System")
print("=================================")

print("\nSelect OS:")
print("1 → macOS")
print("2 → Windows")
print("3 → Linux")

os_choice = input("Enter choice (1/2/3): ").strip()

username = input("Enter your system username: ").strip()

# Build Home Path
if os_choice == "1":
    HOME = f"/Users/{username}"
elif os_choice == "2":
    HOME = f"C:/Users/{username}"
elif os_choice == "3":
    HOME = f"/home/{username}"
else:
    print("Invalid OS choice")
    exit()

# =================================
# ASK FOLDER CHOICE
# =================================
print("\nSelect Folder To Watch:")
print("1 → Downloads")
print("2 → Documents")
print("3 → Desktop")
print("4 → All")

folder_choice = input("Enter choice: ").strip()

WATCH_PATHS = []

if folder_choice == "1":
    WATCH_PATHS.append(os.path.join(HOME, "Downloads"))

elif folder_choice == "2":
    WATCH_PATHS.append(os.path.join(HOME, "Documents"))

elif folder_choice == "3":
    WATCH_PATHS.append(os.path.join(HOME, "Desktop"))

elif folder_choice == "4":
    WATCH_PATHS = [
        os.path.join(HOME, "Downloads"),
        os.path.join(HOME, "Documents"),
        os.path.join(HOME, "Desktop")
    ]

else:
    print("Invalid folder choice")
    exit()

print("\nWatching Paths:")
for p in WATCH_PATHS:
    print("•", p)

# =================================
# LOAD AI MODEL
# =================================
print("\nLoading AI Model...")

model = joblib.load("compression_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

print("AI Model Loaded!")

# =================================
# FEATURE EXTRACTION
# =================================
def calculate_entropy(data):
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(data):
    return [
        len(data),
        calculate_entropy(data),
        len(set(data))
    ]

# =================================
# SKIP FILE TYPES
# =================================
SKIP_EXTENSIONS = (
    ".zip", ".rar", ".7z",
    ".mp4", ".mkv", ".mp3",
    ".jpg", ".png",
    ".br", ".xz", ".zlib"
)

# =================================
# AI COMPRESSION FUNCTION
# =================================
def ai_compress(file_path):

    try:
        if file_path.lower().endswith(SKIP_EXTENSIONS):
            return

        if not os.path.isfile(file_path):
            return

        print("\nDetected File:", file_path)

        with open(file_path, "rb") as f:
            data = f.read()

        if len(data) < 100:
            return

        features = extract_features(data)

        pred = model.predict([features])[0]
        method = label_encoder.inverse_transform([pred])[0]

        print("AI Selected:", method)

        if method == "brotli":
            compressed = brotli.compress(data)
            out_file = file_path + ".br"

        elif method == "zlib":
            compressed = zlib.compress(data)
            out_file = file_path + ".zlib"

        else:
            compressed = lzma.compress(data)
            out_file = file_path + ".xz"

        with open(out_file, "wb") as f:
            f.write(compressed)

        original = len(data)
        comp = len(compressed)
        reduction = ((original - comp) / original) * 100

        print("Original:", original, "bytes")
        print("Compressed:", comp, "bytes")
        print("Reduction:", round(reduction, 2), "%")
        print("Saved:", out_file)

    except Exception as e:
        print("Error:", e)

# =================================
# WATCHDOG HANDLER
# =================================
class WatchHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            ai_compress(event.src_path)

# =================================
# START WATCHER
# =================================
if __name__ == "__main__":

    observer = Observer()
    handler = WatchHandler()

    for path in WATCH_PATHS:
        if os.path.exists(path):
            observer.schedule(handler, path, recursive=True)

    observer.start()

    print("\nAI Autonomous Compression Running...")
    print("Press CTRL + C to Stop\n")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()