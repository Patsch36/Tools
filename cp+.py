import os
import shutil
import argparse


def copy_file(src, dest):
    if not os.path.exists(src):
        print(f"Source file '{src}' does not exist.")
        return

    # Create destination directory if it does not exist
    if not os.path.exists(dest):
        if dest.split('/')[-1].find('.') > 0:
            os.makedirs(os.path.dirname(dest))
        else:
            os.makedirs(dest)

    if os.path.isdir(dest):
        dest = os.path.join(dest, os.path.basename(src))

    # Copy the file
    shutil.copy2(src, dest)
    print(f"Copied '{src}' to '{dest}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy a file to a new location.")
    parser.add_argument("source", help="The source file to copy.")
    parser.add_argument(
        "destination", help="The destination where the file should be copied.")

    args = parser.parse_args()

    src = os.path.expanduser(args.source)
    dst = os.path.expanduser(args.destination)

    copy_file(src, dst)
