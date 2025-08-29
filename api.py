"""
Unsplash API functions
"""
import requests
from PIL import Image
import io
import cv2
import numpy as np
from config import *

def search_unsplash(query):
    """Tìm ảnh từ Unsplash"""
    if UNSPLASH_KEY == "YOUR_ACCESS_KEY":
        return "NO_API_KEY"
        
    headers = {"Authorization": f"Client-ID {UNSPLASH_KEY}"}
    params = {
        "query": query,
        "per_page": IMAGES_PER_PAGE,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(SEARCH_URL, headers=headers, 
                              params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        return f"ERROR: {str(e)}"

def download_image(url):
    """Download ảnh về memory"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Chuyển sang OpenCV
        image = Image.open(io.BytesIO(response.content))
        image = image.convert('RGB')
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return cv2.resize(cv_image, (CAMERA_WIDTH, CAMERA_HEIGHT))
    except Exception as e:
        print(f"Lỗi download: {e}")
        return None