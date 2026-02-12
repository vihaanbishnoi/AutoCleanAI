import os
import csv

from feature_extraction import extract_features
from ai_compression import compress_data

METHODS = ["zlib", "lzma", "brotli", "zstd"]

DATASET_FOLDER = "SilesiaCorpus"
OUTPUT_CSV = "training_data.csv"


def get_best_method(data):

    best_method = None
    best_size = None

    for method in METHODS:

        compressed = compress_data(data, method)

        if compressed is None:
            continue

        size = len(compressed)

        if best_size is None or size < best_size:
            best_size = size
            best_method = method

    return best_method, best_size


def process_dataset():

    rows = []

    for file in os.listdir(DATASET_FOLDER):

        file_path = os.path.join(DATASET_FOLDER, file)

        if os.path.isfile(file_path):

            print("Processing:", file)

            with open(file_path, "rb") as f:
                data = f.read()

            size, entropy, unique_bytes = extract_features(file_path)

            best_method, best_size = get_best_method(data)

            rows.append([
                file,
                size,
                entropy,
                unique_bytes,
                best_method,
                best_size
            ])

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "file",
            "size",
            "entropy",
            "unique_bytes",
            "best_method",
            "best_compressed_size"
        ])

        writer.writerows(rows)

    print("Training dataset created:", OUTPUT_CSV)


if __name__ == "__main__":
    process_dataset()