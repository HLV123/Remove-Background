"""
Main entry point
"""
from gui import BackgroundSelector

def main():
    """Hàm chính"""
    try:
        import requests
        from PIL import Image, ImageTk
        import cv2
        import cvzone
    except ImportError as e:
        print(f"❌ Thiếu thư viện: {e}")
        print("📦 Cài đặt: pip install requests pillow opencv-python cvzone")
        input("Nhấn Enter để thoát...")
        return
    
    app = BackgroundSelector()
    app.run()

if __name__ == "__main__":
    main()