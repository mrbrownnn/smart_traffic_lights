#!/usr/bin/env python3
"""
Script để dọn dẹp Ultralytics repo chỉ giữ lại YOLOv8n detection model
Chạy script này để xóa các file không cần thiết cho YOLOv8n
"""

import os
import shutil
from pathlib import Path

def remove_directory(path):
    """Xóa thư mục và tất cả nội dung bên trong"""
    if os.path.exists(path):
        print(f"🗑️  Xóa thư mục: {path}")
        shutil.rmtree(path)
    else:
        print(f"⚠️  Thư mục không tồn tại: {path}")

def remove_file(path):
    """Xóa file"""
    if os.path.exists(path):
        print(f"🗑️  Xóa file: {path}")
        os.remove(path)
    else:
        print(f"⚠️  File không tồn tại: {path}")

def cleanup_ultralytics_repo():
    """Dọn dẹp repo Ultralytics chỉ giữ YOLOv8n detection"""
    
    print("🚀 Bắt đầu dọn dẹp Ultralytics repo cho YOLOv8n...")
    
    # 1. Xóa các model configs không cần thiết
    print("\n📁 Xóa model configs không cần thiết...")
    model_configs_to_remove = [
        "ultralytics/cfg/models/v3",
        "ultralytics/cfg/models/v5", 
        "ultralytics/cfg/models/v6",
        "ultralytics/cfg/models/v9",
        "ultralytics/cfg/models/v10",
        "ultralytics/cfg/models/11",
        "ultralytics/cfg/models/12",
        "ultralytics/cfg/models/rt-detr"
    ]
    
    for config_dir in model_configs_to_remove:
        remove_directory(config_dir)
    
    # Xóa các file YOLOv8 không cần thiết (giữ lại yolov8.yaml)
    v8_files_to_remove = [
        "ultralytics/cfg/models/v8/yolov8-seg.yaml",
        "ultralytics/cfg/models/v8/yolov8-pose.yaml", 
        "ultralytics/cfg/models/v8/yolov8-cls.yaml",
        "ultralytics/cfg/models/v8/yolov8-obb.yaml",
        "ultralytics/cfg/models/v8/yolov8-world.yaml",
        "ultralytics/cfg/models/v8/yolov8-worldv2.yaml",
        "ultralytics/cfg/models/v8/yolov8-ghost.yaml",
        "ultralytics/cfg/models/v8/yolov8-ghost-p2.yaml",
        "ultralytics/cfg/models/v8/yolov8-ghost-p6.yaml",
        "ultralytics/cfg/models/v8/yolov8-p2.yaml",
        "ultralytics/cfg/models/v8/yolov8-p6.yaml",
        "ultralytics/cfg/models/v8/yolov8-pose-p6.yaml",
        "ultralytics/cfg/models/v8/yolov8-seg-p6.yaml",
        "ultralytics/cfg/models/v8/yolov8-rtdetr.yaml",
        "ultralytics/cfg/models/v8/yolov8-cls-resnet50.yaml",
        "ultralytics/cfg/models/v8/yolov8-cls-resnet101.yaml",
        "ultralytics/cfg/models/v8/yoloe-v8.yaml",
        "ultralytics/cfg/models/v8/yoloe-v8-seg.yaml"
    ]
    
    for file_path in v8_files_to_remove:
        remove_file(file_path)
    
    # 2. Xóa solutions hoàn toàn
    print("\n📁 Xóa solutions...")
    remove_directory("ultralytics/solutions")
    
    # 3. Xóa trackers hoàn toàn
    print("\n📁 Xóa trackers...")
    remove_directory("ultralytics/trackers")
    
    # 4. Xóa toàn bộ examples
    print("\n📁 Xóa examples...")
    remove_directory("examples")
    
    # 5. Xóa assets (chỉ giữ core code)
    print("\n📁 Xóa assets...")
    remove_directory("ultralytics/assets")
    
    # 6. Xóa docs
    print("\n📁 Xóa docs...")
    remove_directory("docs")
    
    # 7. Xóa tests
    print("\n📁 Xóa tests...")
    remove_directory("tests")
    
    # 8. Xóa docker
    print("\n📁 Xóa docker...")
    remove_directory("docker")
    
    # 9. Xóa các file không cần thiết khác
    print("\n📁 Xóa các file không cần thiết khác...")
    other_files_to_remove = [
        "CITATION.cff",
        "CONTRIBUTING.md", 
        "README.zh-CN.md",
        "mkdocs.yml"
    ]
    
    for file_path in other_files_to_remove:
        remove_file(file_path)
    
    print("\n✅ Hoàn thành dọn dẹp!")
    print("\n📋 Các file/thư mục đã được giữ lại (core YOLOv8n):")
    print("   - ultralytics/cfg/models/v8/yolov8.yaml")
    print("   - ultralytics/nn/")
    print("   - ultralytics/engine/")
    print("   - ultralytics/data/")
    print("   - ultralytics/utils/")
    print("   - ultralytics/hub/")
    print("   - ultralytics/models/")
    print("   - README.md")
    print("   - LICENSE")
    print("   - pyproject.toml")
    
    print("\n⚠️  Lưu ý: Bạn cần kiểm tra và cập nhật các import trong code")
    print("   để đảm bảo không có lỗi sau khi dọn dẹp.")

if __name__ == "__main__":
    # Xác nhận trước khi thực hiện
    print("⚠️  CẢNH BÁO: Script này sẽ xóa vĩnh viễn các file/thư mục không cần thiết!")
    print("📁 Thư mục hiện tại:", os.getcwd())
    
    confirm = input("\n❓ Bạn có chắc chắn muốn tiếp tục? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y', 'có']:
        cleanup_ultralytics_repo()
    else:
        print("❌ Hủy bỏ dọn dẹp.")
