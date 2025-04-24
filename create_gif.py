import os
import imageio.v3 as iio
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

# === FOLDER PICKER ===
root = tk.Tk()
root.withdraw()  # Hide the main window

# Set initial folder to the directory where script is running
initial_folder = os.getcwd()

image_dir = filedialog.askdirectory(
    title="Select Folder Containing Images",
    initialdir=initial_folder
)

if not image_dir:
    raise FileNotFoundError("No folder was selected.")

# === OUTPUT FILE NAME ===
output_name = input("Enter the name for the output GIF (without extension), or press Enter to use the folder name: ").strip()
if not output_name:
    output_name = os.path.basename(os.path.abspath(image_dir)) or 'output'

output_filename = f"{output_name}.gif"

# === FIND AND PROCESS IMAGES ===
filenames = sorted([
    os.path.join(image_dir, f)
    for f in os.listdir(image_dir)
    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
])

if not filenames:
    raise FileNotFoundError("No image files found in the selected folder.")

# Resize all images to match the size of the first one
first_image = Image.open(filenames[0]).convert('RGB')
image_size = first_image.size

def resize_image(image, size):
    return image.resize(size, Image.LANCZOS)

images = []
for filename in filenames:
    img = Image.open(filename).convert('RGB')
    img_resized = resize_image(img, image_size)
    images.append(np.array(img_resized))

# Check that all shapes match
shapes = [img.shape for img in images]
print("Image shapes:", shapes)

if len(set(shapes)) > 1:
    raise ValueError("Not all images have the same shape")

# === CREATE GIF ===
iio.imwrite(output_filename, images, duration=0.5, loop=0)
print(f"✅ GIF created successfully: {output_filename}")
