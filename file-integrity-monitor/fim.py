import argparse
import hashlib
from pathlib import Path


def compute_sha256(file_path):
    """Compute the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    try:
        with file_path.open("rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha256.update(byte_block)
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return None
    except OSError:
        print(f"[Error] Could not read: {file_path}")
        return None

    return sha256.hexdigest()


parser = argparse.ArgumentParser(
    description="Compute SHA256 hashes for files and directories."
)

parser.add_argument(
    "paths",
    type=Path,
    nargs="+",
    help="Path to a file/files or directory to compute the SHA256 hash",
)


# Main function to handle the command-line arguments and compute hashes for files and directories.
def main():
    args = parser.parse_args()
    for path in args.paths:
        if not path.exists():
            print(f"Path: {path} does not exist.")
            continue
        if path.is_file():
            hash_value = compute_sha256(path)
            if hash_value is None:
                continue
            print(f"File: {path} | SHA256: {hash_value}")
        elif path.is_dir():
            for file in sorted(path.rglob("*")):
                if file.is_file():
                    hash_value = compute_sha256(file)
                    if hash_value is None:
                        continue
                    print(f"File: {file} | SHA256: {hash_value}")
        else:
            print(f"Path: {path} is neither a file nor a directory.")


if __name__ == "__main__":
    main()
