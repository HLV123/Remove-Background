"""
Image utilities
"""
import cv2
import os
from PIL import Image
import numpy as np
from config import *

def load_local_images():
    """Load ảnh từ thư mục local"""
    images = []
    for folder in IMAGE_FOLDERS:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                if filename.lower().endswith(IMAGE_FORMATS):
                    path = f'{folder}/{filename}'
                    img = cv2.imread(path)
                    if img is not None:
                        images.append((path, filename, img))
    return images

def resize_for_camera(img):
    """Resize cho camera"""
    return cv2.resize(img, (CAMERA_WIDTH, CAMERA_HEIGHT))

def resize_for_display(img):
    """Resize cho hiển thị"""
    return cv2.resize(img, THUMBNAIL_SIZE)

def cv_to_pil(cv_img):
    """OpenCV -> PIL"""
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

def is_image_file(filename):
    """Kiểm tra file ảnh"""
    return filename.lower().endswith(IMAGE_FORMATS)