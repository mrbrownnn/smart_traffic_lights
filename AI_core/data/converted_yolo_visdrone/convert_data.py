"""
Convert VisDrone2019-DET dataset annotations to YOLO format.
(8 fields per line: x, y, w, h, score, category_id, truncation, occlusion)

Author: Thanh Pham
Version: 1.3 (2025-11-11) - Fixed annotations and format structure
"""

import os
import shutil
import cv2
from pathlib import Path
from collections import Counter

# ========================= CONFIG =========================
ANNOTATIONS_DIR = Path(r"E:\visdrone\VisDrone2019-DET-train\annotations")
IMAGES_DIR = Path(r"E:\visdrone\VisDrone2019-DET-train\images")
OUTPUT_DIR = Path(r"E:\visdrone\converted_yolo_visdrone\train")

# Mapping: VisDrone -> YOLO (5 traffic-related classes)
VALID_IDS = {
    3: 0,  # bicycle
    4: 1,  # car
    6: 2,  # truck
    9: 3,  # bus
    10: 4, # motor
}

CLASS_NAMES = ["bicycle", "car", "truck", "bus", "motor"]
# ===========================================================
def prepare_output_dirs():

    for subdir in ["images", "labels"]:
        dir_path = OUTPUT_DIR / subdir
        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created output directories in: {OUTPUT_DIR}")


def convert_annotation(annotation_path: Path, image_dir: Path, label_dir: Path, stats: dict):
    """Convert a single VisDrone annotation file to YOLO format."""
    file_stem = annotation_path.stem
    image_path = image_dir / f"{file_stem}.jpg"
    label_output = label_dir / f"{file_stem}.txt"

    if not image_path.exists():
        stats['missing_images'] += 1
        return False

    image = cv2.imread(str(image_path))
    if image is None:
        stats['unreadable_images'] += 1
        return False

    height, width = image.shape[:2]
    valid_boxes = 0

    with open(annotation_path, "r", encoding="utf-8") as f_in, \
         open(label_output, "w", encoding="utf-8") as f_out:

        for line in f_in:
            parts = line.strip().split(",")
            if len(parts) < 8:
                stats['malformed_lines'] += 1
                continue

            try:
                x, y, w, h, score, cat_id, trunc, occ = map(float, parts[:8])
            except ValueError:
                stats['malformed_lines'] += 1
                continue

            cat_id_int = int(cat_id)
            stats['all_categories'][cat_id_int] += 1

            # Skip ignored regions
            if int(score) == 0:
                stats['ignored_boxes'] += 1
                continue

            if cat_id_int not in VALID_IDS:
                stats['filtered_categories'][cat_id_int] += 1
                continue

            if w <= 0 or h <= 0:
                stats['invalid_dimensions'] += 1
                continue

            if x < 0 or y < 0 or x + w > width or y + h > height:
                stats['out_of_bounds'] += 1
                continue

            cls_id = VALID_IDS[cat_id_int]
            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height
            w_norm = w / width
            h_norm = h / height

            f_out.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
            valid_boxes += 1
            stats['converted_boxes'] += 1

    if valid_boxes == 0:
        stats['empty_files'] += 1

    shutil.copy2(image_path, OUTPUT_DIR / "images" / image_path.name)
    return True

def main():
    if not ANNOTATIONS_DIR.exists() or not IMAGES_DIR.exists():
        print("❌ ERROR: Input directories not found!")
        return

    prepare_output_dirs()
    ann_files = sorted(ANNOTATIONS_DIR.glob("*.txt"))
    if not ann_files:
        print("❌ No annotation files found!")
        return

    print(f"📁 Found {len(ann_files)} annotation files")
    label_dir = OUTPUT_DIR / "labels"

    stats = {
        'missing_images': 0,
        'unreadable_images': 0,
        'malformed_lines': 0,
        'ignored_boxes': 0,
        'filtered_categories': Counter(),
        'all_categories': Counter(),
        'invalid_dimensions': 0,
        'out_of_bounds': 0,
        'converted_boxes': 0,
        'empty_files': 0
    }

    converted = 0
    for i, ann_path in enumerate(ann_files, 1):
        if i % 500 == 0:
            print(f"Processing: {i}/{len(ann_files)}...")
        if convert_annotation(ann_path, IMAGES_DIR, label_dir, stats):
            converted += 1

    print("\n" + "=" * 70)
    print(" CONVERSION COMPLETED")
    print("=" * 70)
    print(f"Total files processed:     {len(ann_files)}")
    print(f"Successfully converted:    {converted}")
    print(f"Total boxes converted:     {stats['converted_boxes']}")
    print(f"Files with no valid boxes: {stats['empty_files']}")

    print("\n📊 FILTERING STATISTICS:")
    print(f"  Ignored boxes (score=0):  {stats['ignored_boxes']}")
    print(f"  Invalid dimensions:        {stats['invalid_dimensions']}")
    print(f"  Out of bounds:             {stats['out_of_bounds']}")

    print("\n CATEGORY DISTRIBUTION:")
    visdrone_classes = {
        1: "pedestrian", 2: "people", 3: "bicycle", 4: "car", 5: "van",
        6: "truck", 7: "tricycle", 8: "awning-tricycle", 9: "bus", 10: "motor"
    }

    for cat_id in sorted(stats['all_categories']):
        name = visdrone_classes.get(cat_id, f"unknown_{cat_id}")
        kept = "✅ KEPT" if cat_id in VALID_IDS else "✗ FILTERED"
        print(f"  {cat_id:2d} ({name:18s}): {stats['all_categories'][cat_id]:6d} [{kept}]")

    print("\n ISSUES:")
    print(f"  Missing images:     {stats['missing_images']}")
    print(f"  Unreadable images:  {stats['unreadable_images']}")
    print(f"  Malformed lines:    {stats['malformed_lines']}")
    print(f"\n Output saved to: {OUTPUT_DIR}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

