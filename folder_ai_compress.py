import joblib
import brotli
import zlib
import lzma
import math
from collections import Counter
import os

print("=================================")
print("AI Folder Compression System")
print("=================================")

# =========================
# LOAD MODEL
# =========================
print("\nLoading AI Model...")

model = joblib.load("compression_model.joblib")
label_encoder = joblib.load("label_encoder.joblib")

print("Model Loaded Successfully!")

# =========================
# FEATURE EXTRACTION
# =========================
def calculate_entropy(data):
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs) if len(data) > 0 else 0

def extract_features(data):
    size = len(data)
    entropy = calculate_entropy(data)
    unique_bytes = len(set(data)) if len(data) > 0 else 0
    return [size, entropy, unique_bytes]

# =========================
# COMPRESS SINGLE FILE
# =========================
def compress_single_file(file_path):

    try:
        with open(file_path, "rb") as f:
            data = f.read()

        if len(data) == 0:
            return 0, 0

        features = extract_features(data)

        predicted_label = model.predict([features])[0]
        method = label_encoder.inverse_transform([predicted_label])[0]

        # Apply compression
        if method == "brotli":
            compressed = brotli.compress(data)
            out_file = file_path + ".br"

        elif method == "zlib":
            compressed = zlib.compress(data)
            out_file = file_path + ".zlib"

        elif method == "lzma":
            compressed = lzma.compress(data)
            out_file = file_path + ".xz"

        else:
            compressed = zlib.compress(data)
            out_file = file_path + ".zlib"

        with open(out_file, "wb") as f:
            f.write(compressed)

        print(f"✔ {os.path.basename(file_path)} → {method}")

        return len(data), len(compressed)

    except Exception as e:
        print(f"❌ Error in {file_path}: {e}")
        return 0, 0

# =========================
# FOLDER COMPRESSION
# =========================
def compress_folder(folder_path):

    if not os.path.exists(folder_path):
        print("❌ Folder not found!")
        return

    total_original = 0
    total_compressed = 0
    file_count = 0

    print("\nScanning Folder...\n")

    for root, dirs, files in os.walk(folder_path):
        for file in files:

            # Skip already compressed files
            if file.endswith((".br", ".xz", ".zlib")):
                continue

            file_path = os.path.join(root, file)

            original, compressed = compress_single_file(file_path)

            total_original += original
            total_compressed += compressed
            file_count += 1

    # =========================
    # SUMMARY
    # =========================
    print("\n=================================")
    print("Folder Compression Completed")
    print("=================================")

    print("Files Processed:", file_count)
    print("Total Original Size:", total_original, "bytes")
    print("Total Compressed Size:", total_compressed, "bytes")

    if total_original > 0:
        reduction = ((total_original - total_compressed) / total_original) * 100
        print(f"Total Reduction: {reduction:.2f}%")

# =========================
# MAIN
# =========================
if __name__ == "__main__":

    folder_name = input("\nEnter folder path to compress: ").strip()
    compress_folder(folder_name)