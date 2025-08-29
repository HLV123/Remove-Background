# 🎨 Background Remover - Ứng dụng xóa phông nền
Ứng dụng Python cho phép bạn thay thế phông nền trong video thời gian thực từ webcam sử dụng AI. Hỗ trợ sử dụng ảnh nền từ thư mục local hoặc tìm kiếm từ Unsplash.
## 🔧 Yêu cầu hệ thống
- Python 3.7+ nhưng đừng quá cao vì nhiều thư viện AI chưa sp bản quá mới 
- Webcam
- Kết nối internet (cho Unsplash)
## ⚙️ Cấu hình
### Unsplash API (Tùy chọn)
Để sử dụng tính năng tìm kiếm ảnh từ Unsplash:
1. Tạo tài khoản tại [Unsplash Developers](https://unsplash.com/developers)
2. Tạo ứng dụng mới và lấy **Access Key**
3. Mở file `config.py` và thay thế:
```python
UNSPLASH_KEY = "your_access_key_here"
```
### Quy trình sử dụng
1. **Chọn ảnh nền**:
   - Tab "🏠 Ảnh Local": Chọn từ thư mục `image/`
   - Tab "🌐 Unsplash": Tìm kiếm và tải ảnh online
2. **Thêm ảnh nền**:
   - Click vào ảnh hoặc nút "➕ Chọn"
   - Có thể chọn nhiều ảnh
3. **Mở camera**:
   - Click "🎥 Mở Camera" khi đã chọn ít nhất 1 ảnh
   - Ứng dụng sẽ hiển thị 2 cửa sổ: gốc và đã xử lý
4. **Điều khiển trong chế độ camera**:
   - `Phím 1`: Ảnh nền trước
   - `Phím 2`: Ảnh nền tiếp theo  
   - `Phím 3`: Thoát về menu chính
## 📋 Thông tin thư viện
- **OpenCV**: Xử lý hình ảnh và video
- **cvzone**: Module AI xóa phông nền  
- **Pillow**: Xử lý ảnh
- **Tkinter**: Giao diện người dùng
- **Requests**: Gọi API Unsplash
- **MediaPipe**: AI nhận dạng người (thông qua cvzone)
