"""
Check integrity of YOLO-converted VisDrone dataset.
Author: Thanh Pham (v2.0)
Date: 2025-11-11

This script verifies:
1. Each image has a corresponding label file (and vice versa).
2. Label format: 5 columns per line.
3. Coordinates in range [0, 1].
4. Class IDs within valid range.
5. Summary of class distribution.

Output:
- Prints summary to console.
- Saves detailed report in check_report.txt.
"""

import os
from pathlib import Path
from collections import Counter
from tqdm import tqdm

# ================= CONFIG =================
ROOT_DIR = Path(r"/visdrone/converted_yolo_visdrone")
SUBSETS = ["train", "val"]
CLASS_NAMES = ["bicycle", "car", "truck", "bus", "motor"]
NUM_CLASSES = len(CLASS_NAMES)


# ==================== PROBLEMS ===============================
"""
- conflict mapping Visdrone label dataset
- merge mapping:
 + dataset1(multi-traffic-view): bicycle, car, bus. lorry with mapping 0,1,2,3
 + dataset2(visdrone):bicycle, car, truck, bus, motorbike
"""
# ======================== FIX DATASET STRAGETIC=======================
""""
    sys mapping:
       0: bicycle
       1: car
       2: truck
       3: bus
       4: motobike
"""
#========================= FIX UNFAIRNESS DATASET ========================
"""
    weight/ratio

        Dataset1:
        ratio {
            bicycle: x 4.5
            car: x 0.5
            bus: x 5.6
            lorry(mapping -> truck): x1.2
        }

        All dataset (total weight)
        ratio {
            bicycle: x 2.5-3
            car: 70k instances
            bus: x 4-5            truck: 1.5-2
            motorbike: x 1.2-1.5
        }

"""
# ==========================================


def check_subset(subset_path: Path):
    """Check one subset (train/val/test)."""
    img_dir = subset_path / "images"
    label_dir = subset_path / "labels"

    img_files = sorted([f.stem for f in img_dir.glob("*.jpg")])
    label_files = sorted([f.stem for f in label_dir.glob("*.txt")])

    img_set, label_set = set(img_files), set(label_files)

    missing_labels = img_set - label_set
    missing_images = label_set - img_set

    stats = Counter()
    invalid_lines = 0

    for label_file in tqdm(label_dir.glob("*.txt"), desc=f"Checking {subset_path.name}"):
        with open(label_file, "r") as f:
            for i, line in enumerate(f, 1):
                parts = line.strip().split()
                if len(parts) != 5:
                    invalid_lines += 1
                    continue
                cls, x, y, w, h = parts
                try:
                    cls = int(cls)
                    x, y, w, h = map(float, (x, y, w, h))
                except ValueError:
                    invalid_lines += 1
                    continue

                if not (0 <= cls < NUM_CLASSES):
                    invalid_lines += 1
                    continue
                if not all(0 <= v <= 1 for v in (x, y, w, h)):
                    invalid_lines += 1
                    continue

                stats[cls] += 1

    summary = {
        "subset": subset_path.name,
        "total_images": len(img_files),
        "total_labels": len(label_files),
        "missing_labels": len(missing_labels),
        "missing_images": len(missing_images),
        "invalid_lines": invalid_lines,
        "class_distribution": {CLASS_NAMES[k]: v for k, v in sorted(stats.items())}
    }

    return summary


def main():
    reports = []
    print("Checking YOLO dataset integrity...\n")
    for subset in SUBSETS:
        subset_path = ROOT_DIR / subset
        if not subset_path.exists():
            print(f" Missing subset folder: {subset}")
            continue

        report = check_subset(subset_path)
        reports.append(report)

    # ===== PRINT SUMMARY =====
    print("\n Dataset Summary:")
    for rep in reports:
        print(f"\n--- {rep['subset'].upper()} ---")
        print(f"Total images: {rep['total_images']}")
        print(f"Total labels: {rep['total_labels']}")
        print(f"Missing labels: {rep['missing_labels']}")
        print(f"Missing images: {rep['missing_images']}")
        print(f"Invalid lines: {rep['invalid_lines']}")
        print("Class distribution:")
        for cls, count in rep["class_distribution"].items():
            print(f"  {cls:<10}: {count}")

    # ===== SAVE REPORT =====
    with open(ROOT_DIR / "check_report.txt", "w") as f:
        for rep in reports:
            f.write(f"--- {rep['subset'].upper()} ---\n")
            for k, v in rep.items():
                if k != "class_distribution":
                    f.write(f"{k}: {v}\n")
                else:
                    f.write("class_distribution:\n")
                    for cls, count in v.items():
                        f.write(f"  {cls:<10}: {count}\n")
            f.write("\n")

    print("\n Check completed. Report saved to check_report.txt")


if __name__ == "__main__":
    main()
