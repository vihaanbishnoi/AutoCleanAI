import brotli
import zlib
import lzma
import os

print("=================================")
print("AI Decompression System")
print("=================================")

# =========================
# DECOMPRESSION FUNCTION
# =========================
def decompress_file(file_path):

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return

    print("\nReading Compressed File...")

    with open(file_path, "rb") as f:
        data = f.read()

    # =========================
    # AUTO DETECT METHOD
    # =========================
    print("Detecting Compression Type...")

    if file_path.endswith(".br"):
        method = "brotli"

    elif file_path.endswith(".zlib"):
        method = "zlib"

    elif file_path.endswith(".xz"):
        method = "lzma"

    else:
        print("❌ Unknown compression format!")
        return

    print("Detected Method:", method)

    # =========================
    # APPLY DECOMPRESSION
    # =========================
    print("\nDecompressing File...")

    try:
        if method == "brotli":
            decompressed = brotli.decompress(data)
            out_file = file_path.replace(".br", "_decompressed")

        elif method == "zlib":
            decompressed = zlib.decompress(data)
            out_file = file_path.replace(".zlib", "_decompressed")

        elif method == "lzma":
            decompressed = lzma.decompress(data)
            out_file = file_path.replace(".xz", "_decompressed")

        # Save file
        with open(out_file, "wb") as f:
            f.write(decompressed)

        print("\n=================================")
        print("Decompression Completed")
        print("=================================")
        print("Output File:", out_file)
        print("Decompressed Size:", len(decompressed), "bytes")

    except Exception as e:
        print("❌ Decompression Failed:", e)


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    file_name = input("\nEnter compressed file path: ").strip()
    decompress_file(file_name)