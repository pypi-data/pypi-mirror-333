import os
import subprocess
from shutil import which

import cv2

from .utils import rotate_360_image


def process_image(image_path, pitch, yaw, roll):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error loading image {image_path}")
        return

    rotated_img = rotate_360_image(img, pitch, yaw, roll)

    # Extract file extension
    file_extension = os.path.splitext(image_path)[-1].lower()
    save_path = os.path.splitext(image_path)[0] + "_adjusted" + file_extension

    # Ensure high-quality saving
    if file_extension in [".jpg", ".jpeg"]:
        cv2.imwrite(save_path, rotated_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    elif file_extension == ".png":
        cv2.imwrite(save_path, rotated_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    else:
        cv2.imwrite(save_path, rotated_img)

    if which("exiftool") is not None:
        subprocess.run(["exiftool", "-TagsFromFile", image_path, save_path], check=True)
        os.remove(f"{save_path}_original")
    else:
        print("ExifTool is not installed or not found in PATH. Image metadata will not be copied.")

    print(f"Image saved as {save_path} with maximum quality!")
