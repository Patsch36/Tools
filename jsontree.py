import os
import json

def directory_tree(path):
    # Create a dictionary to represent the directory tree
    tree = {"name": os.path.basename(path), "type": "directory", "children": []}
    
    try:
        # Scan the directory contents
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    # Add file information to the tree
                    tree["children"].append({"name": entry.name, "type": "file"})
                elif entry.is_dir():
                    # Recursively add directory information to the tree
                    tree["children"].append(directory_tree(entry.path))
    except PermissionError:
        # Ignore directories/files that can't be accessed
        pass
    
    return tree

def main(path):
    # Generate the directory tree
    tree = directory_tree(path)
    # Convert the directory tree to a JSON string
    return json.dumps(tree, indent=4)

if __name__ == "__main__":
    # Get the directory path from the user
    directory = input("Geben Sie das Verzeichnis an: ")
    # Ask the user whether to print or save the output
    _print = input("Print or save to file? (p/s): ")
    # Generate the JSON representation of the directory tree
    json_tree = main(directory)
    if _print == "p":
        # Print the JSON string
        print(json_tree)
    elif _print == "s":
        # Save the JSON string to a file
        with open("directory_tree.json", "w") as file:
            file.write(json_tree)
        print(f"Directory tree saved to 'directory_tree.json'.")
