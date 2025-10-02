import json
import os
from pathlib import Path

def coco_to_yolo(coco_json_path, output_dir, image_width, image_height, category_mapping=None):
    """
    Chuyển đổi annotations từ MS COCO format sang YOLO format
    
    Args:
        coco_json_path: Đường dẫn đến file JSON COCO
        output_dir: Thư mục output để lưu file YOLO
        image_width: Chiều rộng ảnh
        image_height: Chiều cao ảnh
        category_mapping: Dict mapping {coco_category_id: yolo_class_id}
                         Ví dụ: {1: 0, 2: 1, 3: 2, 5: 3}
                         Nếu None, tự động map từ 0
    """
    # Tạo thư mục output nếu chưa có
    os.makedirs(output_dir, exist_ok=True)
    
    # Đọc file COCO JSON
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Tạo category mapping nếu chưa có
    if category_mapping is None:
        # Tự động map: lấy tất cả category_id và map từ 0
        all_category_ids = set()
        for ann in coco_data['annotations']:
            all_category_ids.add(ann['category_id'])
        sorted_ids = sorted(all_category_ids)
        category_mapping = {coco_id: yolo_id for yolo_id, coco_id in enumerate(sorted_ids)}
        print("Auto-generated mapping:")
        for coco_id, yolo_id in category_mapping.items():
            print(f"  COCO category_id {coco_id} -> YOLO class {yolo_id}")
    else:
        print("Using custom mapping:")
        for coco_id, yolo_id in category_mapping.items():
            print(f"  COCO category_id {coco_id} -> YOLO class {yolo_id}")
    
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
            # Sử dụng category_mapping để convert
            coco_category_id = ann['category_id']
            if coco_category_id not in category_mapping:
                print(f"Warning: category_id {coco_category_id} không có trong mapping, bỏ qua!")
                continue
            
            class_id = category_mapping[coco_category_id]
            
            yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}"
            yolo_lines.append(yolo_line)
        
        # Lưu file YOLO (mỗi image một file .txt)
        output_file = os.path.join(output_dir, f"image_{image_id}.txt")
        with open(output_file, 'w') as f:
            f.write('\n'.join(yolo_lines))
        
        print(f"Đã chuyển đổi image_id {image_id}: {len(yolo_lines)} objects")

def convert_single_annotation(ann, image_width, image_height):
    """
    Chuyển đổi một annotation đơn lẻ từ COCO sang YOLO format
    
    Args:
        ann: Dictionary chứa annotation COCO
        image_width: Chiều rộng ảnh
        image_height: Chiều cao ảnh
    
    Returns:
        String YOLO format
    """
    x_min, y_min, width, height = ann['bbox']
    
    # Tính toán và normalize
    x_center = (x_min + width / 2) / image_width
    y_center = (y_min + height / 2) / image_height
    norm_width = width / image_width
    norm_height = height / image_height
    
    class_id = ann['category_id'] - 1
    
    return f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}"


# Ví dụ sử dụng
if __name__ == "__main__":
    # Custom mapping cho dataset drone traffic
    # YOLO classes: 0=car, 1=bus, 2=lorry, 3=cyclist, 4=van
    custom_map = {
        # Bạn cần điền COCO category_id tương ứng
        # Ví dụ:
        # 1: 0,   # car
        # 2: 1,   # bus
        # 3: 2,   # lorry
        # 4: 3,   # cyclist
        # 5: 4    # van
    }
    
    # Trước tiên, chạy check_coco_categories để xem category_id
    print("=== Bước 1: Kiểm tra categories trong file COCO ===")
    with open("dataset/multi_view_traffic/drone-mscoco.json", 'r') as f:
        coco_data = json.load(f)
    
    # Hiển thị categories
    if 'categories' in coco_data:
        print("\nCategories có sẵn:")
        for cat in sorted(coco_data['categories'], key=lambda x: x['id']):
            print(f"  ID {cat['id']}: {cat['name']}")
        
        # Tự động tạo mapping dựa trên tên
        name_to_yolo = {
            'car': 0,
            'bus': 1,
            'lorry': 2,
            'cyclist': 3,
            'van': 4
        }
        
        auto_mapping = {}
        for cat in coco_data['categories']:
            cat_name = cat['name'].lower()
            if cat_name in name_to_yolo:
                auto_mapping[cat['id']] = name_to_yolo[cat_name]
        
        print(f"\nAuto-generated mapping:")
        for coco_id, yolo_id in sorted(auto_mapping.items()):
            cat_name = next(c['name'] for c in coco_data['categories'] if c['id'] == coco_id)
            yolo_names = ['car', 'bus', 'lorry', 'cyclist', 'van']
            print(f"  COCO ID {coco_id} ({cat_name}) -> YOLO class {yolo_id} ({yolo_names[yolo_id]})")
        
        custom_map = auto_mapping
    
    print("\n=== Bước 2: Chuyển đổi sang YOLO format ===")
    coco_to_yolo(
        "data/multi_view_traffic/drone-mscoco.json",
        "./yolofile",
        1920,
        1080,
        category_mapping=custom_map
    )
    
    # Tạo file classes.txt cho YOLOv8
    print("\n=== Bước 3: Tạo file classes.txt ===")
    with open("./yolofile/classes.txt", 'w') as f:
        f.write("car\nbus\nlorry\ncyclist\nvan\n")
    print("Đã tạo file classes.txt với 5 classes: car, bus, lorry, cyclist, van")
    
    print("\n✅ Hoàn thành!")