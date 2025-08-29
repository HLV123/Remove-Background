"""
GUI for background selection
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from api import search_unsplash, download_image
from utils import load_local_images, cv_to_pil, resize_for_display
from camera import Camera
from config import *

class BackgroundSelector:
    def __init__(self):
        self.selected_backgrounds = []
        self.background_names = []
        
        # Main window
        self.root = tk.Tk()
        self.root.title("🎨 Background Remover")
        self.root.geometry(WINDOW_SIZE)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        
        self.setup_ui()
        self.load_local()
        
    def setup_ui(self):
        """Setup GUI"""
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(header, text="🎨 CHỌN ẢNH NỀN", 
                 font=('Arial', 16, 'bold')).pack()
        ttk.Label(header, text="Chọn ảnh nền rồi nhấn 'Mở Camera'",
                 font=('Arial', 10), foreground='gray').pack(pady=5)
        
        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Local tab
        self.local_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.local_frame, text="📁 Ảnh Local")
        self.setup_local_tab()
        
        # Unsplash tab
        self.unsplash_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.unsplash_frame, text="🌐 Unsplash")
        self.setup_unsplash_tab()
        
        # Bottom controls
        bottom = ttk.Frame(self.root)
        bottom.pack(fill='x', pady=10, padx=10)
        
        self.count_label = ttk.Label(bottom, text="📸 Đã chọn: 0 ảnh",
                                    font=('Arial', 11, 'bold'))
        self.count_label.pack(pady=(0, 10))
        
        # Buttons
        btn_frame = ttk.Frame(bottom)
        btn_frame.pack()
        
        self.camera_btn = ttk.Button(btn_frame, text="🎥 Mở Camera", 
                                   command=self.open_camera, state='disabled')
        self.camera_btn.pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="🗑️ Xóa Tất Cả", 
                  command=self.clear_all).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="❌ Thoát", 
                  command=self.quit).pack(side='left', padx=5)
    
    def setup_local_tab(self):
        """Setup local images tab"""
        canvas = tk.Canvas(self.local_frame)
        scrollbar = ttk.Scrollbar(self.local_frame, orient="vertical", command=canvas.yview)
        self.local_content = ttk.Frame(canvas)
        
        self.local_content.bind("<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.local_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_unsplash_tab(self):
        """Setup Unsplash tab"""
        # Search
        search_frame = ttk.Frame(self.unsplash_frame)
        search_frame.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(search_frame, text="🔍 Tìm:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=(10, 5))
        self.search_entry.bind('<Return>', self.search)
        
        ttk.Button(search_frame, text="Tìm", command=self.search).pack(side='left')
        
        # Results
        canvas = tk.Canvas(self.unsplash_frame)
        scrollbar = ttk.Scrollbar(self.unsplash_frame, orient="vertical", command=canvas.yview)
        self.unsplash_content = ttk.Frame(canvas)
        
        self.unsplash_content.bind("<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.unsplash_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")
        
        # Initial message
        self.show_message(self.unsplash_content, 
            "💡 Nhập từ khóa và Enter để tìm\nVD: nature, city, space...")
    
    def load_local(self):
        """Load local images"""
        # Clear
        for widget in self.local_content.winfo_children():
            widget.destroy()
        
        images = load_local_images()
        
        if not images:
            self.show_message(self.local_content, 
                "📁 Không có ảnh trong thư mục 'image'\nThêm ảnh vào thư mục đó")
            return
        
        # Display grid
        for i, (path, name, img) in enumerate(images):
            self.create_image_item(self.local_content, img, f"Local: {name}", 
                                 i // GRID_COLS, i % GRID_COLS, is_local=True)
    
    def create_image_item(self, parent, cv_img, name, row, col, is_local=False):
        """Create image item"""
        frame = ttk.Frame(parent, relief='ridge', borderwidth=2)
        frame.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
        parent.grid_columnconfigure(col, weight=1)
        
        try:
            # Display image
            display_img = resize_for_display(cv_img) if is_local else cv_img
            pil_img = cv_to_pil(display_img)
            pil_img = pil_img.resize(THUMBNAIL_SIZE)
            photo = ImageTk.PhotoImage(pil_img)
            
            # Image label
            img_label = ttk.Label(frame, image=photo, cursor="hand2")
            img_label.image = photo
            img_label.pack(pady=5)
            
            # Name
            display_name = name if len(name) <= 25 else name[:22] + "..."
            ttk.Label(frame, text=display_name, font=('Arial', 9), 
                     anchor='center', wraplength=180).pack(pady=(0, 5))
            
            # Button
            ttk.Button(frame, text="➕ Chọn", 
                      command=lambda: self.add_background(cv_img, name)).pack(pady=(0, 5))
            
            # Click to select
            img_label.bind("<Button-1>", lambda e: self.add_background(cv_img, name))
            
        except Exception as e:
            ttk.Label(frame, text=f"❌ Lỗi: {str(e)}", wraplength=180).pack(pady=20)
    
    def search(self, event=None):
        """Search Unsplash"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Cảnh báo", "Nhập từ khóa!")
            return
        
        self.show_message(self.unsplash_content, "🔄 Đang tìm...")
        
        def search_thread():
            results = search_unsplash(query)
            self.root.after(0, lambda: self.show_results(results))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def show_results(self, results):
        """Show search results"""
        # Clear
        for widget in self.unsplash_content.winfo_children():
            widget.destroy()
        
        if results == "NO_API_KEY":
            self.show_message(self.unsplash_content, 
                "🔑 Cần API key!\nSửa UNSPLASH_KEY trong config.py")
            return
        elif isinstance(results, str) and results.startswith("ERROR"):
            self.show_message(self.unsplash_content, f"❌ Lỗi: {results[7:]}")
            return
        elif not results:
            self.show_message(self.unsplash_content, "🔍 Không tìm thấy\nThử từ khóa khác")
            return
        
        # Display results
        for i, img_data in enumerate(results):
            self.create_unsplash_item(self.unsplash_content, img_data, 
                                    i // GRID_COLS, i % GRID_COLS)
    
    def create_unsplash_item(self, parent, img_data, row, col):
        """Create Unsplash item"""
        frame = ttk.Frame(parent, relief='ridge', borderwidth=2)
        frame.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
        parent.grid_columnconfigure(col, weight=1)
        
        def load_and_display():
            try:
                # Load thumbnail
                import requests
                import io
                response = requests.get(img_data['urls']['thumb'], timeout=10)
                pil_img = Image.open(io.BytesIO(response.content))
                pil_img = pil_img.resize(THUMBNAIL_SIZE)
                photo = ImageTk.PhotoImage(pil_img)
                
                # Image
                img_label = ttk.Label(frame, image=photo, cursor="hand2")
                img_label.image = photo
                img_label.pack(pady=5)
                
                # Author
                author = img_data['user']['name']
                display_author = author if len(author) <= 20 else author[:17] + "..."
                ttk.Label(frame, text=f"📸 {display_author}", font=('Arial', 9)).pack()
                
                # Button
                ttk.Button(frame, text="➕ Chọn", 
                          command=lambda: self.download_and_add(img_data)).pack(pady=5)
                
                # Click
                img_label.bind("<Button-1>", lambda e: self.download_and_add(img_data))
                
            except Exception:
                ttk.Label(frame, text="❌ Lỗi tải", font=('Arial', 9)).pack(pady=20)
        
        threading.Thread(target=load_and_display, daemon=True).start()
    
    def download_and_add(self, img_data):
        """Download and add Unsplash image"""
        def download():
            try:
                cv_img = download_image(img_data['urls']['regular'])
                if cv_img is not None:
                    author = img_data['user']['name']
                    self.root.after(0, lambda: self.add_background(cv_img, f"Unsplash: {author}"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Lỗi", "Không tải được ảnh"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi: {str(e)}"))
        
        threading.Thread(target=download, daemon=True).start()
    
    def add_background(self, cv_img, name):
        """Add background to selection"""
        if name in self.background_names:
            messagebox.showinfo("Thông báo", f"Đã có: {name}")
            return
        
        from utils import resize_for_camera
        self.selected_backgrounds.append(resize_for_camera(cv_img))
        self.background_names.append(name)
        
        self.update_count()
        messagebox.showinfo("Thành công", f"✅ Đã thêm: {name}")
    
    def update_count(self):
        """Update count label"""
        count = len(self.selected_backgrounds)
        self.count_label.config(text=f"📸 Đã chọn: {count} ảnh")
        self.camera_btn.config(state='normal' if count > 0 else 'disabled')
    
    def clear_all(self):
        """Clear all selected"""
        if not self.selected_backgrounds:
            messagebox.showinfo("Thông báo", "Chưa có ảnh nào!")
            return
            
        if messagebox.askyesno("Xác nhận", f"Xóa {len(self.selected_backgrounds)} ảnh?"):
            self.selected_backgrounds.clear()
            self.background_names.clear()
            self.update_count()
    
    def open_camera(self):
        """Open camera"""
        if not self.selected_backgrounds:
            messagebox.showwarning("Cảnh báo", "Chưa chọn ảnh!")
            return
        
        self.root.withdraw()
        camera = Camera(self.selected_backgrounds, self.background_names, self.show_window)
        camera.run()
    
    def show_window(self):
        """Show main window"""
        self.root.deiconify()
    
    def show_message(self, parent, text):
        """Show message in frame"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(parent)
        frame.pack(expand=True, fill='both', pady=50)
        ttk.Label(frame, text=text, font=('Arial', 11), 
                 anchor='center', justify='center').pack()
    
    def quit(self):
        """Quit app"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run app"""
        self.update_count()
        self.root.mainloop()