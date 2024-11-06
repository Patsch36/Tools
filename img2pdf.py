import os
import sys
import time
from PIL import Image
from fpdf import FPDF
import shutil

PDF_SIZE = (210, 297)  # A4 size in mm
SPACING = 10  # Space between images in mm

# Get the image paths from command-line arguments or use images from ./imgs folder
if len(sys.argv) > 1:
    img_paths = []
    for path in sys.argv[1:]:
        if os.path.exists(path):
            img_paths.append(path)
        else:
            print(f"Image path '{path}' does not exist.")
else:
    try:
        img_paths = [os.path.join('./imgs', img) for img in os.listdir('./imgs')]
    except FileNotFoundError:
        print(f"No 'imgs' folder found at {os.getcwd()}. Please create a folder named 'imgs' and place your images in it.")
        exit()

img_paths.sort(key=lambda x: os.path.getctime(x))

# Convert images to PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for img_path in img_paths:
    pdf.add_page()

    # Get the original image size
    img_obj = Image.open(img_path)
    img_width, img_height = img_obj.size

    # Calculate the aspect ratio to maintain the original size
    aspect_ratio = img_width / img_height

    # Calculate the new width and height based on the page size (210x297)
    if aspect_ratio > 1:
        new_width = (PDF_SIZE[0] - 2 * SPACING)
        new_height = (PDF_SIZE[0] - 2 * SPACING) / aspect_ratio
    else:
        new_width = (PDF_SIZE[1] - 2 * SPACING) * aspect_ratio
        new_height = (PDF_SIZE[1] - 2 * SPACING)

    # Add the image to the PDF with the calculated size
    pdf.image(img_path, SPACING, SPACING, new_width, new_height)

# Create output folder
folder = os.getcwd() + "/output_" + time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime())
if not os.path.exists(folder):
    os.makedirs(folder)

# Save PDF
pdf.output(f"{folder}/output.pdf", "F")
print(f"PDF saved to {folder}/output.pdf")

# Copy images to output folder
if len(sys.argv) < 1:
    shutil.copytree('./imgs', folder + '/imgs')
else:
    for img_path in img_paths:
        shutil.copy(img_path, folder)

# Delete images in imgs folder
for img_path in img_paths:
    try:
        os.remove(img_path)
    except OSError as e:
        # print(f"Error deleting {img_path}: {e}")
        pass
