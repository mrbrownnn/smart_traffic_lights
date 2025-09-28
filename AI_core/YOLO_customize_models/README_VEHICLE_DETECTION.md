# YOLOv8n Vehicle Detection & Counting

Hướng dẫn sử dụng YOLOv8n để phát hiện và đếm phương tiện giao thông.

## 🚗 Các loại phương tiện được phát hiện

Theo COCO dataset, YOLOv8n có thể phát hiện các loại phương tiện sau:
- **Car** (ID: 2) - Ô tô
- **Motorcycle** (ID: 3) - Xe máy  
- **Bus** (ID: 5) - Xe buýt
- **Truck** (ID: 7) - Xe tải

## 📋 Yêu cầu hệ thống

```bash
pip install ultralytics opencv-python
```

## 🚀 Cách sử dụng

### 1. Phát hiện phương tiện đơn giản

```bash
# Phát hiện từ webcam
python vehicle_detection_counter.py --source 0 --mode detect --show

# Phát hiện từ video file
python vehicle_detection_counter.py --source "traffic.mp4" --mode detect --show --save

# Sử dụng GPU
python vehicle_detection_counter.py --source "traffic.mp4" --device 0 --mode detect --show
```

### 2. Đếm phương tiện qua đường thẳng

```bash
# Đếm từ webcam
python vehicle_detection_counter.py --source 0 --mode line --show

# Đếm từ video và lưu kết quả
python vehicle_detection_counter.py --source "traffic.mp4" --mode line --show --save
```

### 3. Đếm phương tiện trong vùng xác định

```bash
# Đếm trong các vùng từ webcam
python vehicle_detection_counter.py --source 0 --mode region --show

# Đếm trong các vùng từ video
python vehicle_detection_counter.py --source "traffic.mp4" --mode region --show --save
```

## ⚙️ Tham số cấu hình

| Tham số | Mô tả | Mặc định |
|---------|-------|----------|
| `--source` | Nguồn video (0=webcam, đường dẫn file) | `0` |
| `--model` | Đường dẫn model YOLOv8n | `yolov8n.pt` |
| `--device` | Thiết bị xử lý (cpu, 0, 1, ...) | `cpu` |
| `--mode` | Chế độ: detect, line, region | `detect` |
| `--show` | Hiển thị kết quả | `False` |
| `--save` | Lưu kết quả ra file | `False` |

## 🎯 Các chế độ hoạt động

### 1. Detect Mode
- Phát hiện và vẽ bounding box cho tất cả phương tiện
- Hiển thị confidence score và class name
- Không đếm số lượng

### 2. Line Mode  
- Đếm phương tiện đi qua một đường thẳng
- Phân biệt hướng vào/ra
- Hiển thị tổng số đếm được

### 3. Region Mode
- Đếm phương tiện trong các vùng đa giác xác định
- Hỗ trợ nhiều vùng cùng lúc
- Mỗi vùng có màu sắc riêng

## 🔧 Tùy chỉnh

### Thay đổi điểm đường đếm (Line Mode)
```python
# Trong file vehicle_detection_counter.py, dòng 67
line_points = [(100, 400), (800, 400)]  # Thay đổi tọa độ theo video
```

### Thay đổi vùng đếm (Region Mode)
```python
# Trong file vehicle_detection_counter.py, dòng 120-130
counter.add_region(
    name="Zone1",
    polygon=[(100, 100), (400, 100), (400, 300), (100, 300)],  # Thay đổi tọa độ
    color=(255, 0, 0),  # Thay đổi màu
    text_color=(255, 255, 255)
)
```

### Thay đổi confidence threshold
```python
# Trong file vehicle_detection_counter.py, dòng 35
conf=0.5  # Thay đổi từ 0.0 đến 1.0
```

## 📊 Kết quả

### Detect Mode
- Hiển thị bounding box và label cho mỗi phương tiện
- Confidence score cho mỗi detection

### Line Mode
- Tổng số phương tiện vào
- Tổng số phương tiện ra  
- Tổng cộng

### Region Mode
- Số lượng phương tiện trong mỗi vùng
- Tổng số track được phát hiện

## 🎥 Ví dụ sử dụng

```bash
# Phát hiện phương tiện từ webcam
python vehicle_detection_counter.py --source 0 --mode detect --show

# Đếm phương tiện qua đường từ video file
python vehicle_detection_counter.py --source "highway.mp4" --mode line --show --save

# Đếm phương tiện trong 2 vùng từ video
python vehicle_detection_counter.py --source "parking.mp4" --mode region --show --save

# Sử dụng GPU để tăng tốc
python vehicle_detection_counter.py --source "traffic.mp4" --device 0 --mode line --show
```

## 🚨 Lưu ý

1. **Điểm đường đếm**: Cần điều chỉnh tọa độ `line_points` phù hợp với video
2. **Vùng đếm**: Cần điều chỉnh `polygon` phù hợp với vùng quan tâm
3. **Confidence**: Giảm `conf` nếu muốn phát hiện nhiều hơn (có thể có false positive)
4. **Performance**: Sử dụng GPU (`--device 0`) để tăng tốc xử lý
5. **Video format**: Hỗ trợ hầu hết format video (mp4, avi, mov, ...)

## 🔍 Troubleshooting

### Lỗi "Không thể mở video"
- Kiểm tra đường dẫn file video
- Đảm bảo file video tồn tại và không bị hỏng
- Thử với webcam trước (`--source 0`)

### Kết quả đếm không chính xác
- Điều chỉnh `line_points` hoặc `polygon` phù hợp với video
- Thay đổi `conf` threshold
- Kiểm tra chất lượng video (độ phân giải, ánh sáng)

### Hiệu suất chậm
- Sử dụng GPU: `--device 0`
- Giảm độ phân giải video
- Tăng `conf` threshold để giảm số detection
