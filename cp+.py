import os
import shutil
import argparse


def copy_file_or_directory(src, dest):
    if not os.path.exists(src):
        print(f"Source '{src}' does not exist.")
        return

    # Create destination directory if it does not exist
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    if os.path.isdir(src):
        # Copy the directory
        dest = os.path.join(dest, os.path.basename(src))
        shutil.copytree(src, dest)
        print(f"Copied directory '{src}' to '{dest}'")
    else:
        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(src))
        # Copy the file
        shutil.copy2(src, dest)
        print(f"Copied file '{src}' to '{dest}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy a file or directory to a new location.")
    parser.add_argument("source", help="The source file or directory to copy.")
    parser.add_argument(
        "destination", help="The destination where the file or directory should be copied.")

    args = parser.parse_args()

    src = os.path.expanduser(args.source)
    dst = os.path.expanduser(args.destination)

    copy_file_or_directory(src, dst)
