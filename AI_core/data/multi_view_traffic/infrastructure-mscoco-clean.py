import json
from tqdm import tqdm

# === Input / Output ===
input_file = "infrastructure-mscoco.json"
output_file = "infrastructure-mscoco-clean.json"

with open(input_file, "r") as f:
    coco = json.load(f)

images = {img["id"]: img for img in coco["images"]}
categories = coco["categories"]

valid_categories = [c for c in categories if c["name"].lower() != "unlabeled"]
valid_cat_ids = {c["id"] for c in valid_categories}

clean_annotations = []

for ann in tqdm(coco["annotations"]):
    # Inspector category
    if ann["category_id"] not in valid_cat_ids:
        continue
    
    # bbox = [x, y, w, h]
    x, y, w, h = ann["bbox"]
    if w <= 0 or h <= 0:
        continue
    
    if ann["image_id"] not in images:
        continue
    
    img_info = images[ann["image_id"]]
    if x + w > img_info["width"] or y + h > img_info["height"]:
        continue
    
    
    new_ann = {
        "id": ann["id"],
        "image_id": ann["image_id"],
        "category_id": ann["category_id"],
        "bbox": [x, y, w, h],
        "area": ann.get("area", w * h),
        "iscrowd": ann.get("iscrowd", 0),
        "segmentation": ann.get("segmentation", [])
    }
    clean_annotations.append(new_ann)

coco_clean = {
    "images": list(images.values()),
    "annotations": clean_annotations,
    "categories": valid_categories
}

with open(output_file, "w") as f:
    json.dump(coco_clean, f, indent=2)

print(f"Done! ")
print(f"Annotations original: {len(coco['annotations'])} -> After cleaning: {len(clean_annotations)}")
