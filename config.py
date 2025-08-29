"""
Configuration settings
"""

# Unsplash API
UNSPLASH_KEY = ""  # Thay bằng API key thật

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CUT_THRESHOLD = 0.8

# GUI settings
WINDOW_SIZE = "900x700"
THUMBNAIL_SIZE = (200, 150)
GRID_COLS = 3

# File settings
IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
IMAGE_FOLDERS = ["image", "images"]

# API settings
SEARCH_URL = "https://api.unsplash.com/search/photos"
IMAGES_PER_PAGE = 12
TIMEOUT = 10