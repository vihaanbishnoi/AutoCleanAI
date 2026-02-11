from scanner import scan_folder
from exact_duplicates import find_exact_duplicates
from embedding import get_image_embedding
from clustering import cluster_embeddings
from similarity import calculate_similarity
from decision_engine import select_best_file
from deletion_manager import move_to_quarantine
import numpy as np


folders_to_scan = [
    r"C:\Users\Beriwal\Downloads",
    r"C:\Users\Beriwal\Desktop"
]


def run_cleanup():

    all_files = []

    for folder in folders_to_scan:
        print(f"\nScanning: {folder}")
        files = scan_folder(folder)
        all_files.extend(files)

    if not all_files:
        print("No image files found.")
        return

    # ----------------------------
    # 1️⃣ EXACT DUPLICATES
    # ----------------------------
    print("\nChecking exact duplicates...")
    exact_duplicates = find_exact_duplicates(all_files)

    for group in exact_duplicates:
        best = select_best_file(group)

        print("\nExact Duplicate Group Found:")
        for file in group:
            print("   ", file)
        print("Similarity: 100.00%")

        confirm = input("Remove duplicates except best file? (yes/no): ").lower()

        if confirm == "yes":
            for file in group:
                if file != best:
                    move_to_quarantine(file)
            print("Duplicates moved to quarantine.")
        else:
            print("Skipped this group.")

    # Re-scan after exact duplicate handling
    all_files = []
    for folder in folders_to_scan:
        files = scan_folder(folder)
        all_files.extend(files)

    # ----------------------------
    # 2️⃣ AI NEAR DUPLICATES
    # ----------------------------
    print("\nExtracting embeddings...")

    embeddings = []
    valid_files = []

    for file in all_files:
        embedding = get_image_embedding(file)
        if embedding is not None:
            embeddings.append(embedding)
            valid_files.append(file)

    if len(embeddings) < 2:
        print("Not enough files for AI clustering.")
        return

    embeddings = np.array(embeddings)
    clusters = cluster_embeddings(valid_files, embeddings)

    print("\nProcessing near-duplicate clusters...")

    for cluster in clusters.values():
        paths = [item[0] for item in cluster]
        emb_list = [item[1] for item in cluster]

        best = select_best_file(paths)

        print("\nNear-Duplicate Cluster Found:")

        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                similarity = calculate_similarity(
                    emb_list[i],
                    emb_list[j]
                )
                print(f"{paths[i]} <-> {paths[j]} : {similarity:.2f}% similar")

        confirm = input("Remove duplicates except best file? (yes/no): ").lower()

        if confirm == "yes":
            for file in paths:
                if file != best:
                    move_to_quarantine(file)
            print("Duplicates moved to quarantine.")
        else:
            print("Skipped this cluster.")

    print("\nCleanup cycle complete.")


if __name__ == "__main__":
    run_cleanup()
