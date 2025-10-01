import json
import os
from pathlib import Path

def initparameters():
    coco_json_path = "drone-mscoco.json"
    output_dir = "./yolofile/drone"
    image_width = 1920
    image_height = 1080
    return coco_json_path, output_dir, image_width, image_height

def coco_to_yolo(coco_json_path, output_dir, image_width, image_height):
    """
    Chuyển đổi annotations từ MS COCO format sang YOLO format
    
    Args:
        coco_json_path: Đường dẫn đến file JSON COCO
        output_dir: Thư mục output để lưu file YOLO
        image_width: Chiều rộng ảnh
        image_height: Chiều cao ảnh
    """
    # Tạo thư mục output nếu chưa có
    os.makedirs(output_dir, exist_ok=True)  # Sửa: makedir -> makedirs
    
    # Đọc file COCO JSON
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Nhóm annotations theo image_id
    annotations_by_image = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)
    
    # Chuyển đổi từng image
    for image_id, annotations in annotations_by_image.items():
        yolo_lines = []
        
        for ann in annotations:
            # Lấy thông tin bbox từ COCO (x_min, y_min, width, height)
            x_min, y_min, width, height = ann['bbox']
            
            # Tính toán center point và normalize
            x_center = (x_min + width / 2) / image_width
            y_center = (y_min + height / 2) / image_height
            norm_width = width / image_width
            norm_height = height / image_height
            
            # YOLO format: class_id x_center y_center width height
            # COCO category_id thường bắt đầu từ 1, YOLO class_id bắt đầu từ 0
            class_id = ann['category_id'] - 1
            
            yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}"
            yolo_lines.append(yolo_line)
        
        # Lưu file YOLO (mỗi image một file .txt)
        output_file = os.path.join(output_dir, f"image_{image_id}.txt")
        with open(output_file, 'w') as f:
            f.write('\n'.join(yolo_lines))
        
        print(f"Đã chuyển đổi image_id {image_id}: {len(yolo_lines)} objects")

# Chạy chương trình
if __name__ == "__main__":
    coco_json_path, output_dir, image_width, image_height = initparameters()
    coco_to_yolo(coco_json_path, output_dir, image_width, image_height)
    print("Done!")