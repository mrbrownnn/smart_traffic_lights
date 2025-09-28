#!/usr/bin/env python3
"""
Script để cập nhật các import không cần thiết sau khi dọn dẹp
Loại bỏ các import cho segmentation, pose, obb, classification, etc.
"""

import os
import re
from pathlib import Path

def update_imports_in_file(file_path):
    """Cập nhật imports trong một file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Loại bỏ các import không cần thiết cho YOLOv8n detection
        imports_to_remove = [
            # Segmentation
            'Segment', 'YOLOESegment', 'v8SegmentationLoss', 'SegmentationModel',
            # Pose
            'Pose', 'v8PoseLoss', 'PoseModel', 
            # OBB
            'OBB', 'v8OBBLoss', 'OBBModel',
            # Classification  
            'Classify', 'v8ClassificationLoss', 'ClassificationModel',
            # World/CLIP
            'WorldDetect', 'WorldModel', 'ImagePoolingAttn', 'C2fAttn',
            # YOLOE
            'YOLOEDetect', 'YOLOEModel', 'YOLOESegModel',
            # RTDETR
            'RTDETRDecoder', 'RTDETRDetectionModel',
            # v10
            'v10Detect',
            # Other modules not needed for YOLOv8n
            'AIFI', 'C2PSA', 'C2fPSA', 'C2fCIB', 'C2fAttn', 'C3TR', 'C3Ghost',
            'C3x', 'RepC3', 'RepNCSPELAN4', 'ELAN1', 'ADown', 'AConv', 'SPPELAN',
            'CBFuse', 'CBLinear', 'A2C2f', 'SCDown', 'TorchVision', 'Index',
            'LRPCHead', 'ResNetLayer', 'RepVGGDW', 'GhostBottleneck', 'GhostConv',
            'HGBlock', 'HGStem', 'Focus', 'BottleneckCSP', 'C1', 'C2', 'C3',
            'C3k2', 'DWConvTranspose2d', 'ConvTranspose', 'Conv2',
            # Loss functions
            'E2EDetectLoss'
        ]
        
        # Cập nhật imports trong ultralytics/nn/tasks.py
        if 'ultralytics/nn/tasks.py' in str(file_path):
            # Loại bỏ các import không cần thiết
            for import_name in imports_to_remove:
                # Loại bỏ từ import list
                content = re.sub(rf',\s*{import_name}', '', content)
                content = re.sub(rf'{import_name}\s*,', '', content)
                content = re.sub(rf'from.*import.*{import_name}.*\n', '', content)
            
            # Loại bỏ các class không cần thiết
            classes_to_remove = [
                'SegmentationModel', 'PoseModel', 'OBBModel', 'ClassificationModel',
                'RTDETRDetectionModel', 'WorldModel', 'YOLOEModel', 'YOLOESegModel'
            ]
            
            for class_name in classes_to_remove:
                # Tìm và loại bỏ class definition
                pattern = rf'class {class_name}\(.*?\):.*?(?=class|\Z)'
                content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Cập nhật imports trong ultralytics/nn/modules/__init__.py
        if 'ultralytics/nn/modules/__init__.py' in str(file_path):
            for import_name in imports_to_remove:
                content = re.sub(rf',\s*{import_name}', '', content)
                content = re.sub(rf'{import_name}\s*,', '', content)
        
        # Cập nhật imports trong ultralytics/cfg/__init__.py
        if 'ultralytics/cfg/__init__.py' in str(file_path):
            # Loại bỏ các task không cần thiết
            content = re.sub(r'"segment"', '', content)
            content = re.sub(r'"classify"', '', content) 
            content = re.sub(r'"pose"', '', content)
            content = re.sub(r'"obb"', '', content)
            content = re.sub(r',\s*,', ',', content)  # Loại bỏ dấu phẩy thừa
        
        # Ghi file nếu có thay đổi
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Đã cập nhật: {file_path}")
            return True
        else:
            print(f"⏭️  Không cần cập nhật: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật {file_path}: {e}")
        return False

def cleanup_imports():
    """Dọn dẹp imports trong toàn bộ repo"""
    
    print("🔧 Bắt đầu cập nhật imports...")
    
    # Các file cần cập nhật imports
    files_to_update = [
        "ultralytics/nn/tasks.py",
        "ultralytics/nn/modules/__init__.py", 
        "ultralytics/cfg/__init__.py",
        "ultralytics/__init__.py"
    ]
    
    updated_count = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_imports_in_file(file_path):
                updated_count += 1
        else:
            print(f"⚠️  File không tồn tại: {file_path}")
    
    print(f"\n✅ Hoàn thành! Đã cập nhật {updated_count} file(s)")
    print("\n📋 Các thay đổi chính:")
    print("   - Loại bỏ imports cho segmentation, pose, obb, classification")
    print("   - Loại bỏ các class model không cần thiết")
    print("   - Cập nhật task definitions")
    
    print("\n⚠️  Lưu ý: Hãy kiểm tra lại code để đảm bảo không có lỗi import!")

if __name__ == "__main__":
    cleanup_imports()
