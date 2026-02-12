import os
import pandas as pd
import numpy as np
import brotli
import zlib
import lzma
import math
from collections import Counter

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
    return size, entropy, unique_bytes

# =========================
# COMPRESSION METHODS
# =========================
def compress_all(data):
    results = {}

    try:
        results["brotli"] = len(brotli.compress(data))
    except:
        results["brotli"] = 999999999

    try:
        results["zlib"] = len(zlib.compress(data))
    except:
        results["zlib"] = 999999999

    try:
        results["lzma"] = len(lzma.compress(data))
    except:
        results["lzma"] = 999999999

    return results

# =========================
# CHUNK SETTINGS
# =========================
CHUNK_SIZE = 1024 * 1024   # 1MB chunks

DATASET = []

DATA_FOLDER = "SilesiaCorpus"

print("Scanning dataset folder...")

for root, dirs, files in os.walk(DATA_FOLDER):
    for file in files:

        filepath = os.path.join(root, file)

        try:
            with open(filepath, "rb") as f:
                data = f.read()
        except:
            continue

        file_size = len(data)
        chunks = max(1, file_size // CHUNK_SIZE)

        print(f"Processing {file} → {chunks} chunks")

        for i in range(chunks):
            start = i * CHUNK_SIZE
            end = start + CHUNK_SIZE
            chunk = data[start:end]

            if len(chunk) < 100:
                continue

            size, entropy, unique_bytes = extract_features(chunk)

            comp_results = compress_all(chunk)

            best_method = min(comp_results, key=comp_results.get)
            best_size = comp_results[best_method]

            DATASET.append([
                file + f"_chunk{i}",
                size,
                entropy,
                unique_bytes,
                best_method,
                best_size
            ])

# =========================
# SAVE CSV
# =========================
df = pd.DataFrame(DATASET, columns=[
    "file",
    "size",
    "entropy",
    "unique_bytes",
    "best_method",
    "best_compressed_size"
])

df.to_csv("training_data.csv", index=False)

print("✅ New dataset generated")
print("Total rows:", len(df))