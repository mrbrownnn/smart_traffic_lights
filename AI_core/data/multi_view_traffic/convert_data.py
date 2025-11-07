"""
# This Python script converts object detection annotations from the COCO JSON format to the YOLO text format.
It reads bounding box information from a COCO dataset, maps selected category IDs to YOLO class IDs, and writes normalized coordinates (x_center, y_center, width, height) into .txt label files.

For each annotation:

The corresponding image file is also copied into the output directory to ensure each label has a matching image.
Unsupported categories are skipped based on the valid_ids mapping.
The script processes two datasets:
Drone dataset

Infrastructure dataset
Each converted dataset contains two subfolders:
converted_yolo_2/
├── drone/
│   ├── *.jpg (images)
│   └── *.txt (YOLO labels)
└── infrastructure/
    ├── *.jpg
    └── *.txt
This script is typically used to prepare COCO-labeled traffic datasets (e.g., cars, buses, trucks, motorcycles) for YOLOv8/YOLOv11 training.
"""

from pathlib import Path
import json
import os
import shutil 
def convert(json_path, img_root, out_root, valid_ids):
    os.makedirs(out_root, exist_ok=True)
    label_dir =Path(out_root)
    image_out_dir = Path(out_root)
    label_dir.mkdir(parents=True,exist_ok=True)
    image_out_dir.mkdir(parents=True, exist_ok=True)

    with open(json_path, "r") as f:
        data = json.load(f)

    image_map = {img["id"]: img for img in data["images"]}
    converted, skipped = 0, 0

#core convert 
    for ann in data["annotations"]:
        cat_id = ann["category_id"]
        if cat_id not in valid_ids:
            skipped += 1
            continue
    
        img_info = image_map[ann["image_id"]]
        file_name = os.path.basename(img_info["file_name"])  
        file_stem = os.path.splitext(file_name)[0]
        w, h = img_info["width"], img_info["height"]

        x, y, bw, bh = ann["bbox"]
        x_c = (x + bw / 2) / w
        y_c = (y + bh / 2) / h
        bw /= w
        bh /= h
        cls_id = valid_ids[cat_id]

        out_file = label_dir/ f"{file_stem}.txt"
        with open(out_file,"a") as f:
            f.write( f"{cls_id} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n")
        src_image = Path(img_root) / file_name
        des_image = image_out_dir /file_name

        #LOOP FUNCTION: audit per object are existed or not
        if src_image.exists() and not des_image.exists():
            shutil.copy(src_image,des_image)
        
        converted +=1
        print(f"Converting: {file_name} -> {out_file}")

    print(f"{json_path} done. Converted {converted}, skipped {skipped}")

# Mapping COCO ids -> YOLO ids
valid_ids = {2:0, 3:1, 6:2, 8:3}



# Convert drone
convert(
    json_path="C:/Users/admin/Desktop/project_local_backup/AI_core/data/multi_view_traffic/drone-mscoco.json",
    img_root="C:/Users/admin/Desktop/project_local_backup/AI_core/data/multi_view_traffic/converted_yolo(2)/drone_images",
    out_root="C:/Users/admin/Desktop/project_local_backup/AI_core/data/multi_view_traffic/converted_yolo_2/drone",
    valid_ids=valid_ids
)

# Convert infrastructure
convert(
    json_path=r"C:/Users/admin/Desktop/project_local_backup/AI_core/data/multi_view_traffic/infrastructure-mscoco.json",
    img_root=r"C:/Users/admin/Desktop/project_local_backup/AI_core/data/multi_view_traffic/converted_yolo(2)//Infrastructure",
    out_root=r"C:/Users/admin/Desktop/project_local_backup/AI_core\data/multi_view_traffic/converted_yolo_2/infrastructure",
    valid_ids=valid_ids
)
""" COCOS to YOLO format
{
  "class": {
    "0": "person",
    "1": "bicycle",
    "2": "car",
    "3": "motorcycle",
    "4": "airplane",
    "5": "bus",
    "6": "train",
    "7": "truck",
    "8": "boat",
    "9": "traffic light",
    "10": "fire hydrant",
    "11": "stop sign",
    "12": "parking meter",
    "13": "bench",
    "14": "bird",
    "15": "cat",
    "16": "dog",
    "17": "horse",
    "18": "sheep",
    "19": "cow",
    "20": "elephant",
    "21": "bear",
    "22": "zebra",
    "23": "giraffe",
    "24": "backpack",
    "25": "umbrella",
    "26": "handbag",
    "27": "tie",
    "28": "suitcase",
    "29": "frisbee",
    "30": "skis",
    "31": "snowboard",
    "32": "sports ball",
    "33": "kite",
    "34": "baseball bat",
    "35": "baseball glove",
    "36": "skateboard",
    "37": "surfboard",
    "38": "tennis racket",
    "39": "bottle",
    "40": "wine glass",
    "41": "cup",
    "42": "fork",
    "43": "knife",
    "44": "spoon",
    "45": "bowl",
    "46": "banana",
    "47": "apple",
    "48": "sandwich",
    "49": "orange",
    "50": "brocolli",
    "51": "carrot",
    "52": "hot dog",
    "53": "pizza",
    "54": "donut",
    "55": "cake",
    "56": "chair",
    "57": "couch",
    "58": "potted plant",
    "59": "bed",
    "60": "dining table",
    "61": "toilet",
    "62": "tv",
    "63": "laptop",
    "64": "mouse",
    "65": "remote",
    "66": "keyboard",
    "67": "cell phone",
    "68": "microwave",
    "69": "oven",
    "70": "toaster",
    "71": "sink",
    "72": "refrigerator",
    "73": "book",
    "74": "clock",
    "75": "vase",
    "76": "scissors",
    "77": "teddy bear",
    "78": "hair drier",
    "79": "toothbrush"
  }
}
"""