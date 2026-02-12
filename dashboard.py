# dashboard.py
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from autonomous_ai_compress import ai_compress
from smart_ai_decompress import decompress_file, open_file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =========================
# TRACKER CLASS
# =========================
class Tracker:
    def __init__(self):
        self.already_compressed = set()
        self.already_decompressed = set()

    def add_compressed(self, path, reduction):
        self.already_compressed.add(path)

    def add_decompressed(self, path):
        self.already_decompressed.add(path)

tracker = Tracker()

# =========================
# GUI CLASS
# =========================
class DashboardApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Compression Dashboard")
        self.root.geometry("800x600")

        self.tree = ttk.Treeview(self.root, columns=("Status"), show="headings")
        self.tree.heading("Status", text="Status / Info")
        self.tree.pack(fill="both", expand=True)

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side="bottom", pady=10)

    def add_to_list(self, text):
        self.tree.insert("", tk.END, values=(text,))

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

# =========================
# WATCHDOG HANDLER
# =========================
class UnifiedHandler(FileSystemEventHandler):
    def __init__(self, tracker, app):
        self.tracker = tracker
        self.app = app
        self.last_processed = {}  # file_path: timestamp

    def _can_process(self, path):
        basename = os.path.basename(path)
        if "/__pycache__/" in path or basename.startswith(".") or path.endswith(".tmp") or basename.startswith("~$"):
            return False
        now = time.time()
        if path in self.last_processed and now - self.last_processed[path] < 5:
            return False
        self.last_processed[path] = now
        return True

    def on_created(self, event):
        if event.is_directory:
            return
        path = event.src_path
        # Compress new normal files
        if self._can_process(path) and not path.endswith((".br", ".zlib", ".xz")):
            if path not in self.tracker.already_compressed:
                out_file, reduction = ai_compress(path)
                if out_file:
                    self.tracker.add_compressed(out_file, reduction)
                    self.app.add_to_list(f"Compressed: {out_file} → {round(reduction,2)}% reduction")
        # Decompress new compressed files
        elif path.endswith((".br", ".zlib", ".xz")):
            if path not in self.tracker.already_decompressed:
                restored = decompress_file(path)
                if restored:
                    self.tracker.add_decompressed(restored)
                    self.app.add_to_list(f"Decompressed: {restored}")
                    try:
                        open_file(restored)
                    except:
                        pass

    def on_modified(self, event):
        if event.is_directory:
            return
        path = event.src_path
        # Only decompress modified compressed files
        if path.endswith((".br", ".zlib", ".xz")) and self._can_process(path):
            if path not in self.tracker.already_decompressed:
                restored = decompress_file(path)
                if restored:
                    self.tracker.add_decompressed(restored)
                    self.app.add_to_list(f"Decompressed: {restored}")
                    try:
                        open_file(restored)
                    except:
                        pass

# =========================
# WATCHER THREAD
# =========================
def start_watchers(tracker, app):
    HOME = os.path.expanduser("~")
    WATCH_FOLDERS = [
        os.path.join(HOME, "Downloads"),
        os.path.join(HOME, "Documents"),
        os.path.join(HOME, "Desktop")
    ]
    observer = Observer()
    handler = UnifiedHandler(tracker, app)
    for folder in WATCH_FOLDERS:
        if os.path.exists(folder):
            observer.schedule(handler, folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app = DashboardApp()
    threading.Thread(target=start_watchers, args=(tracker, app), daemon=True).start()
    app.root.mainloop()