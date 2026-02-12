from scanner import scan_folder
from exact_duplicates import find_exact_duplicates
from embedding import get_image_embedding
from document_embedding import get_document_embedding
from clustering import cluster_embeddings
from similarity import calculate_similarity
from decision_engine import select_best_file
from deletion_manager import move_to_quarantine

import numpy as np


# 🔥 FOLDERS TO SCAN
folders_to_scan = [
    r"C:\Users\Beriwal\Downloads",
    r"C:\Users\Beriwal\Desktop"
]


def ask_confirmation():
    while True:
        confirm = input("Remove duplicates except best file? (yes/no): ").strip().lower()
        if confirm in ["yes", "no"]:
            return confirm
        else:
            print("Please type 'yes' or 'no'.")


def run_cleanup():

    print("\n==============================")
    print(" AI Duplicate Detection System")
    print("==============================\n")

    all_files = []

    # ----------------------------
    # SCAN ALL TARGET FOLDERS
    # ----------------------------
    for folder in folders_to_scan:
        print(f"Scanning: {folder}")
        files = scan_folder(folder)
        all_files.extend(files)

    if not all_files:
        print("No supported files found.")
        return

    # ==================================================
    # 1️⃣ EXACT DUPLICATE DETECTION
    # ==================================================
    print("\nChecking exact duplicates (SHA-256)...")

    exact_duplicates = find_exact_duplicates(all_files)

    for group in exact_duplicates:
        best = select_best_file(group)

        print("\nExact Duplicate Group Found:")
        for file in group:
            print("   ", file)
        print("Similarity: 100.00%")

        confirm = ask_confirmation()

        if confirm == "yes":
            for file in group:
                if file != best:
                    move_to_quarantine(file)
            print("Duplicates moved to quarantine.")
        else:
            print("Skipped this group.")

    # Re-scan after exact duplicate removal
    all_files = []
    for folder in folders_to_scan:
        files = scan_folder(folder)
        all_files.extend(files)

    # ==================================================
    # 2️⃣ IMAGE NEAR DUPLICATES (AI)
    # ==================================================
    print("\nProcessing image files...")

    image_files = [
        f for f in all_files
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    image_embeddings = []
    valid_image_files = []

    for file in image_files:
        emb = get_image_embedding(file)
        if emb is not None:
            image_embeddings.append(emb)
            valid_image_files.append(file)

    if len(image_embeddings) >= 2:
        image_embeddings = np.array(image_embeddings)
        image_clusters = cluster_embeddings(valid_image_files, image_embeddings)

        for cluster in image_clusters.values():
            paths = [item[0] for item in cluster]
            emb_list = [item[1] for item in cluster]

            best = select_best_file(paths)

            print("\nImage Duplicate Cluster Found:")
            for i in range(len(paths)):
                for j in range(i + 1, len(paths)):
                    similarity = calculate_similarity(
                        emb_list[i],
                        emb_list[j]
                    )
                    print(f"{paths[i]} <-> {paths[j]} : {similarity:.2f}% similar")

            confirm = ask_confirmation()

            if confirm == "yes":
                for file in paths:
                    if file != best:
                        move_to_quarantine(file)
                print("Image duplicates moved to quarantine.")
            else:
                print("Skipped image cluster.")

    # ==================================================
    # 3️⃣ DOCUMENT NEAR DUPLICATES (TXT / PDF / DOCX)
    # ==================================================
    print("\nProcessing document files...")

    document_files = [
        f for f in all_files
        if f.lower().endswith(('.txt', '.pdf', '.docx'))
    ]

    doc_embeddings = []
    valid_doc_files = []

    for file in document_files:
        emb = get_document_embedding(file)
        if emb is not None:
            doc_embeddings.append(emb)
            valid_doc_files.append(file)

    if len(doc_embeddings) >= 2:
        doc_embeddings = np.array(doc_embeddings)
        doc_clusters = cluster_embeddings(valid_doc_files, doc_embeddings)

        for cluster in doc_clusters.values():
            paths = [item[0] for item in cluster]
            emb_list = [item[1] for item in cluster]

            best = select_best_file(paths)

            print("\nDocument Duplicate Cluster Found:")
            for i in range(len(paths)):
                for j in range(i + 1, len(paths)):
                    similarity = calculate_similarity(
                        emb_list[i],
                        emb_list[j]
                    )
                    print(f"{paths[i]} <-> {paths[j]} : {similarity:.2f}% similar")

            confirm = ask_confirmation()

            if confirm == "yes":
                for file in paths:
                    if file != best:
                        move_to_quarantine(file)
                print("Document duplicates moved to quarantine.")
            else:
                print("Skipped document cluster.")

    print("\nCleanup cycle complete.\n")


if __name__ == "__main__":
    run_cleanup()
