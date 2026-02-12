import joblib
import brotli
import zlib
import lzma
import math
from collections import Counter
import os

print("=================================")
print(" AI Compression Prediction System ")
print("=================================")

# =========================
# LOAD MODEL
# =========================
try:
    print("\nLoading AI Model...")
    model = joblib.load("compression_model.joblib")
    label_encoder = joblib.load("label_encoder.joblib")
    print("✅ Model Loaded Successfully!")
except:
    print("❌ Model files not found. Run training first.")
    exit()

# =========================
# FEATURE EXTRACTION
# =========================
def calculate_entropy(data):
    if len(data) == 0:
        return 0
    counts = Counter(data)
    probs = [c / len(data) for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def extract_features(data):
    size = len(data)
    entropy = calculate_entropy(data)
    unique_bytes = len(set(data))
    return [size, entropy, unique_bytes]

# =========================
# COMPRESSION FUNCTION
# =========================
def compress_file(file_path):

    file_path = os.path.abspath(file_path)

    # File existence check
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return

    print("\n📂 Reading File...")
    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) == 0:
        print("❌ File is empty")
        return

    print("📊 Extracting Features...")
    features = extract_features(data)

    print("🧠 Predicting Best Compression Method...")
    predicted_label = model.predict([features])[0]
    method = label_encoder.inverse_transform([predicted_label])[0]

    print("✅ Predicted Method:", method)

    # =========================
    # APPLY COMPRESSION
    # =========================
    print("\n⚙ Compressing File...")

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
        print("⚠ Unknown Method → Using ZLIB fallback")
        compressed = zlib.compress(data)
        out_file = file_path + ".zlib"

    # Save file
    with open(out_file, "wb") as f:
        f.write(compressed)

    # =========================
    # METRICS CALCULATION
    # =========================
    original_size = len(data)
    compressed_size = len(compressed)

    reduction = original_size - compressed_size
    reduction_percent = (reduction / original_size) * 100
    ratio = compressed_size / original_size

    # =========================
    # OUTPUT RESULTS
    # =========================
    print("\n=================================")
    print(" ✅ Compression Completed")
    print("=================================")

    print("📄 Output File:", out_file)
    print("📦 Original Size:", original_size, "bytes")
    print("🗜 Compressed Size:", compressed_size, "bytes")
    print("📉 Size Reduced:", reduction, "bytes")
    print("📊 Reduction Percentage:", round(reduction_percent, 2), "%")
    print("⚖ Compression Ratio:", round(ratio, 3))

# =========================
# MAIN RUN
# =========================
if __name__ == "__main__":

    file_name = input("\nEnter file path to compress: ").strip()
    compress_file(file_name)