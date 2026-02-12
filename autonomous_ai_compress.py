# autonomous_ai_compress.py
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

# =========================
# DEFAULT WATCH PATHS (for imports / dashboard)
# =========================
HOME = os.path.expanduser("~")
WATCH_PATHS = [
    os.path.join(HOME, "Downloads"),
    os.path.join(HOME, "Documents"),
    os.path.join(HOME, "Desktop")
]

# =========================
# LOAD AI MODEL
# =========================
model = joblib.load("compression_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# =========================
# SKIP EXTENSIONS
# =========================
SKIP_EXTENSIONS = (
    ".zip", ".rar", ".7z",
    ".mp4", ".mkv", ".mp3",
    ".jpg", ".png",
    ".br", ".xz", ".zlib"
)

# =========================
# FEATURE EXTRACTION
# =========================
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

# =========================
# AI COMPRESSION FUNCTION
# =========================
def ai_compress(file_path):
    """Compress a file using AI-selected method. Returns (compressed_file, reduction%)."""
    try:
        if file_path.lower().endswith(SKIP_EXTENSIONS):
            return None, 0
        if not os.path.isfile(file_path):
            return None, 0

        with open(file_path, "rb") as f:
            data = f.read()
        if len(data) < 100:
            return None, 0

        features = extract_features(data)
        pred = model.predict([features])[0]
        method = label_encoder.inverse_transform([pred])[0]

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
        return out_file, reduction

    except Exception as e:
        print("Compression error:", e)
        return None, 0

# =========================
# WATCHDOG HANDLER
# =========================
class WatchHandler(FileSystemEventHandler):
    def __init__(self, tracker=None):
        self.tracker = tracker

    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            out_file, reduction = ai_compress(event.src_path)
            if self.tracker and out_file:
                self.tracker.add_compressed(out_file, reduction)

# =========================
# MAIN (standalone mode)
# =========================
if __name__ == "__main__":
    print("Universal AI Compression System")

    # --- Ask OS + username ---
    os_choice = input("Select OS (1 macOS / 2 Windows / 3 Linux): ").strip()
    username = input("Enter username: ").strip()

    if os_choice == "1":
        HOME = f"/Users/{username}"
    elif os_choice == "2":
        HOME = f"C:/Users/{username}"
    elif os_choice == "3":
        HOME = f"/home/{username}"
    else:
        print("Invalid OS choice")
        exit()

    # --- Ask folders to watch ---
    folder_choice = input("Select folder (1 Downloads / 2 Documents / 3 Desktop / 4 All): ").strip()
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

    # --- Start Watcher ---
    observer = Observer()
    handler = WatchHandler()
    for path in WATCH_PATHS:
        if os.path.exists(path):
            observer.schedule(handler, path, recursive=True)
    observer.start()

    print("AI Autonomous Compression Running...")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()