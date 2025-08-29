"""
Camera app with background removal
"""
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from tkinter import messagebox
from config import *

class Camera:
    def __init__(self, backgrounds, names, callback):
        self.backgrounds = backgrounds
        self.names = names
        self.callback = callback
        self.current_index = 0
        self.segmentor = SelfiSegmentation()
        
    def run(self):
        """Chạy camera"""
        cap = cv2.VideoCapture(0)
        cap.set(3, CAMERA_WIDTH)
        cap.set(4, CAMERA_HEIGHT)
        
        if not cap.isOpened():
            messagebox.showerror("Lỗi", "Không thể mở camera!")
            self.callback()
            return
        
        print(f"🎥 Camera mở với {len(self.backgrounds)} ảnh nền")
        print("1=Trước, 2=Sau, 3=Thoát")
        
        while True:
            success, img = cap.read()
            if not success:
                break
            
            # Remove background
            bg = self.backgrounds[self.current_index]
            img_out = self.segmentor.removeBG(img, bg, cutThreshold=CUT_THRESHOLD)
            
            # Hiển thị info
            name = self.names[self.current_index]
            if len(name) > 35:
                name = name[:32] + "..."
                
            info = f"{self.current_index + 1}/{len(self.backgrounds)}: {name}"
            cv2.putText(img_out, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (255, 255, 255), 1)
            
            # Stack images
            stacked = cvzone.stackImages([img, img_out], 2, 1)
            cv2.imshow("Background Remover - Press 3 to return", stacked)
            
            # Controls
            key = cv2.waitKey(1) & 0xFF
            if key == ord("1"):
                self.current_index = (self.current_index - 1) % len(self.backgrounds)
            elif key == ord("2"):
                self.current_index = (self.current_index + 1) % len(self.backgrounds)
            elif key == ord("3"):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.callback()