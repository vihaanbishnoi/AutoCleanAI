import zlib
import lzma
import brotli
import zstandard as zstd


# -----------------------------
# Individual Compression Methods
# -----------------------------

def compress_zlib(data):
    return zlib.compress(data)


def compress_lzma(data):
    return lzma.compress(data)


def compress_brotli(data):
    return brotli.compress(data)


def compress_zstd(data):
    cctx = zstd.ZstdCompressor()
    return cctx.compress(data)


# -----------------------------
# Universal Compression Function
# -----------------------------

def compress_data(data, method):

    if method == "zlib":
        return compress_zlib(data)

    elif method == "lzma":
        return compress_lzma(data)

    elif method == "brotli":
        return compress_brotli(data)

    elif method == "zstd":
        return compress_zstd(data)

    else:
        return None


# -----------------------------
# File Compression Helper
# -----------------------------

def compress_file(file_path, method):

    with open(file_path, "rb") as f:
        data = f.read()

    compressed = compress_data(data, method)

    if compressed is None:
        print("Invalid compression method")
        return

    out = file_path + "." + method

    with open(out, "wb") as f:
        f.write(compressed)

    print("Compressed using:", method)
    print("Original Size:", len(data))
    print("Compressed Size:", len(compressed))


# -----------------------------
# Test Run
# -----------------------------

if __name__ == "__main__":

    # Change file name if needed
    test_file = "sample.txt"

    compress_file(test_file, "zstd")