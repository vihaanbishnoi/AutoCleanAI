import numpy as np
from collections import Counter


# -----------------------------
# Entropy Calculation
# -----------------------------

def calculate_entropy(data):

    if len(data) == 0:
        return 0

    counter = Counter(data)
    probs = [count / len(data) for count in counter.values()]

    entropy = -sum(p * np.log2(p) for p in probs)

    return entropy


# -----------------------------
# Feature Extraction Main Function
# -----------------------------

def extract_features(file_path):

    with open(file_path, "rb") as f:
        data = f.read()

    size = len(data)
    entropy = calculate_entropy(data)
    unique_bytes = len(set(data))

    return size, entropy, unique_bytes


# -----------------------------
# Test Run
# -----------------------------

if __name__ == "__main__":

    file = "sample.txt"

    size, entropy, unique = extract_features(file)

    print("File Size:", size)
    print("Entropy:", entropy)
    print("Unique Bytes:", unique)