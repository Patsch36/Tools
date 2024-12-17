import os
import shutil
import argparse


def move_file_or_directory(src, dest):
    if not os.path.exists(src):
        print(f"Source '{src}' does not exist.")
        return

    # Create destination directory if it does not exist
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    if os.path.isdir(src):
        # Move the directory
        dest = os.path.join(dest, os.path.basename(src))
        shutil.move(src, dest)
        print(f"Moved directory '{src}' to '{dest}'")
    else:
        if os.path.isdir(dest):
            dest = os.path.join(dest, os.path.basename(src))
        # Move the file
        shutil.move(src, dest)
        print(f"Moved file '{src}' to '{dest}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move a file or directory to a new location.")
    parser.add_argument("source", help="The source file or directory to move.")
    parser.add_argument(
        "destination", help="The destination where the file or directory should be moved.")

    args = parser.parse_args()

    src = os.path.expanduser(args.source)
    dst = os.path.expanduser(args.destination)

    move_file_or_directory(src, dst)
