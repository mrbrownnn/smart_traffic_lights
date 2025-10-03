from pathlib import Path
import json, os

def convert(json_path, img_root, out_root, valid_ids):
    os.makedirs(out_root, exist_ok=True)

    with open(json_path, "r") as f:
        data = json.load(f)

    image_map = {img["id"]: img for img in data["images"]}
    converted, skipped = 0, 0

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

        out_file = os.path.join(out_root, f"{file_stem}.txt")
        print("Converting:", file_name, "->", out_file)
        with open(out_file, "a") as f:
            f.write(f"{cls_id} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n")

        converted += 1

    print(f"✅ {json_path} done. Converted {converted}, skipped {skipped}.")


# Mapping COCO ids -> YOLO ids
valid_ids = {2:0, 3:1, 6:2, 8:3}

# Convert drone
convert(
    json_path="E:/multi_view_traffic/drone-mscoco.json",
    img_root="E:/multi_view_traffic/Drone",
    out_root="E:/multi_view_traffic/converted_yolo/drone_labels",
    valid_ids=valid_ids
)

# Convert infrastructure
convert(
    json_path="E:/multi_view_traffic/infrastructure-mscoco.json",
    img_root="E:/multi_view_traffic/Infrastructure",
    out_root="E:/multi_view_traffic/converted_yolo/infrastructure_labels",
    valid_ids=valid_ids
)
