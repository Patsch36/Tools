import os
import shutil
import argparse


def move_file(src, dest):
    if not os.path.exists(src):
        print(f"Source file '{src}' does not exist.")
        return

    # Create destination directory if it does not exist
    if not os.path.exists(dest):
        if len(os.path.splitext(dest.split('/')[-1])[1])>0:
            if len(dest.split('/'))>1:
                os.makedirs(os.path.dirname(dest.split('/')[0:-1]))
        else:
            os.makedirs(dest)

    if os.path.isdir(dest):
        dest = os.path.join(dest, os.path.basename(src))

    # Move the file
    shutil.move(src, dest)
    print(f"Moved '{src}' to '{dest}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move a file to a new location.")
    parser.add_argument("source", help="The source file to move.")
    parser.add_argument(
        "destination", help="The destination where the file should be moved.")

    args = parser.parse_args()

    src = os.path.expanduser(args.source)
    dst = os.path.expanduser(args.destination)

    move_file(src, dst)
