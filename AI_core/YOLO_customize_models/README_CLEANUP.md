# Hướng dẫn dọn dẹp Ultralytics cho YOLOv8n

## Tổng quan

Repo Ultralytics chứa rất nhiều model variants và tasks không cần thiết nếu bạn chỉ muốn sử dụng YOLOv8n cho object detection. Script này sẽ giúp bạn dọn dẹp repo để chỉ giữ lại những gì cần thiết.

## Các file sẽ bị xóa

### 1. Model Configs không cần thiết
- `ultralytics/cfg/models/v3/` - YOLOv3
- `ultralytics/cfg/models/v5/` - YOLOv5  
- `ultralytics/cfg/models/v6/` - YOLOv6
- `ultralytics/cfg/models/v9/` - YOLOv9
- `ultralytics/cfg/models/v10/` - YOLOv10
- `ultralytics/cfg/models/11/` - YOLO11
- `ultralytics/cfg/models/12/` - YOLO12
- `ultralytics/cfg/models/rt-detr/` - RT-DETR

### 2. YOLOv8 variants không cần thiết
- `yolov8-seg.yaml` - Segmentation
- `yolov8-pose.yaml` - Pose estimation
- `yolov8-cls.yaml` - Classification
- `yolov8-obb.yaml` - Oriented bounding boxes
- `yolov8-world.yaml` - World models
- `yolov8-ghost.yaml` - Ghost variants
- `yolov8-p2.yaml`, `yolov8-p6.yaml` - P2/P6 variants
- `yoloe-v8.yaml` - YOLOE variants

### 3. Thư mục không cần thiết
- `ultralytics/solutions/` - Các solution modules
- `ultralytics/trackers/` - Tracking modules
- `examples/` - Example code
- `docs/` - Documentation
- `tests/` - Test files
- `docker/` - Docker files

### 4. Files không cần thiết
- `CITATION.cff`
- `CONTRIBUTING.md`
- `README.zh-CN.md`
- `mkdocs.yml`

## Các file sẽ được giữ lại

### Core YOLOv8n files
- `ultralytics/cfg/models/v8/yolov8.yaml` - YOLOv8n config
- `ultralytics/nn/tasks.py` - DetectionModel class
- `ultralytics/nn/modules/` - Core modules (Detect, C2f, SPPF, Conv, etc.)
- `ultralytics/engine/` - Training/validation engine
- `ultralytics/data/` - Data handling
- `ultralytics/utils/` - Utilities
- `ultralytics/hub/` - Model hub
- `ultralytics/models/` - Model classes

### Essential files
- `README.md`
- `LICENSE`
- `pyproject.toml`

## Cách sử dụng

### Bước 1: Backup repo
```bash
cp -r ultralytics ultralytics_backup
```

### Bước 2: Chạy script dọn dẹp
```bash
python cleanup_yolov8n.py
```

### Bước 3: Cập nhật imports
```bash
python cleanup_imports.py
```

### Bước 4: Kiểm tra và test
```bash
python -c "from ultralytics import YOLO; model = YOLO('yolov8n.yaml')"
```

## Lưu ý quan trọng

1. **Backup trước khi chạy**: Script sẽ xóa vĩnh viễn các file
2. **Kiểm tra imports**: Sau khi dọn dẹp, cần kiểm tra các import
3. **Test model**: Đảm bảo YOLOv8n vẫn hoạt động bình thường
4. **Git**: Nếu dùng git, commit trước khi chạy script

## Kết quả mong đợi

Sau khi dọn dẹp, repo sẽ nhỏ hơn đáng kể và chỉ chứa:
- YOLOv8n detection model
- Core modules cần thiết
- Training/validation pipeline
- Essential utilities

## Troubleshooting

### Lỗi import
Nếu gặp lỗi import sau khi dọn dẹp:
1. Kiểm tra file `ultralytics/nn/modules/__init__.py`
2. Kiểm tra file `ultralytics/nn/tasks.py`
3. Chạy lại `cleanup_imports.py`

### Lỗi model loading
Nếu không load được model:
1. Kiểm tra file `ultralytics/cfg/models/v8/yolov8.yaml`
2. Kiểm tra các dependencies trong `pyproject.toml`

### Khôi phục từ backup
Nếu cần khôi phục:
```bash
rm -rf ultralytics
mv ultralytics_backup ultralytics
```
