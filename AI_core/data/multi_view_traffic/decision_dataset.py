"""
Split YOLO dataset (flat structure) into train/validation/test subsets.

This script:
1. Reads images (.jpg) and labels (.txt) stored together in each folder (e.g., 'drone/', 'infrastructure/').
2. Randomly splits each dataset into train (70%) and validation (30%).
3. Randomly selects 500 image–label pairs for testing.
4. Generates data.yaml (for training) and data_test.yaml (inside sample_2000/ for testing).

Author by: Thanh Pham

"""
"""
Split YOLO dataset (flat structure) into train/validation/test subsets.

Author: Thanh Pham
"""

import os
import shutil
import random
import yaml
from pathlib import Path

# ====================== CONFIG ======================
BASE_PATH = Path(__file__).resolve().parent
BASE_DIR = BASE_PATH / "converted_yolo_2"
OUTPUT_DIR = BASE_PATH / "split_yolo_v2"
SOURCE_FOLDERS = ["drone", "infrastructure"]

TRAIN_RATIO = 0.7
SAMPLE_SIZE = 500
CLASS_NAMES = ["bicycle", "car", "bus", "lorry"]
# ====================================================


def prepare_output_folders():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    for split in ["train", "val", "sample_500/train", "sample_500/val"]:
        for subfolder in ["images", "labels"]:
            os.makedirs(OUTPUT_DIR / split / subfolder, exist_ok=True)


def copy_image_and_label(label_path: Path, split_name: str, folder_root: Path):
    img_name = label_path.stem + ".jpg"
    img_src = folder_root / img_name
    lbl_src = folder_root / label_path.name
    img_dst = OUTPUT_DIR / split_name / "images" / img_name
    lbl_dst = OUTPUT_DIR / split_name / "labels" / label_path.name
    if lbl_src.exists():
        shutil.copy2(lbl_src, lbl_dst)
    if img_src.exists():
        shutil.copy2(img_src, img_dst)


def generate_yaml(yaml_path: Path, path_root: str, train_rel: str, val_rel: str):
    """create YAML file with proper metadata header"""
    header = f"""# Traffic Detection Dataset (converted from MSCOCO)
# Author: Thanh Pham
# Version: 2025-10-06
# Description:
#   Dataset split 70/30 into train/val
#   Converted from MSCOCO via valid_ids = {{2:0, 3:1, 6:2, 8:3}}
#   Structure:
#       split_yolo/
#           ├── train/images
#           ├── train/labels
#           ├── val/images
#           └── val/labels

# Root dataset path (Colab path)
path: {path_root}
"""
    data_yaml = {
        "train": train_rel,
        "val": val_rel,
        "nc": len(CLASS_NAMES),
        "names": {i: name for i, name in enumerate(CLASS_NAMES)},
        "download": ""
    }
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.dump(data_yaml, f, allow_unicode=True, sort_keys=False)
    print(f"Created {yaml_path.name} at {yaml_path.parent}")


def split_dataset():
    prepare_output_folders()
    stats = {}
    all_labels = []

    # ====== STEP 1: Split main train/val ======
    for subset in SOURCE_FOLDERS:
        folder = BASE_DIR / subset
        lbls = [folder / f for f in os.listdir(folder) if f.endswith(".txt")]
        random.shuffle(lbls)

        n = len(lbls)
        n_train = int(n * TRAIN_RATIO)
        train_lbls = lbls[:n_train]
        val_lbls = lbls[n_train:]

        for f in train_lbls:
            copy_image_and_label(f, "train", folder)
        for f in val_lbls:
            copy_image_and_label(f, "val", folder)

        stats[subset] = {"total": n, "train": len(train_lbls), "val": len(val_lbls)}
        all_labels.extend(lbls)

    # ====== STEP 2: Split sample_500 into train/val (70:30) ======
    if len(all_labels) >= SAMPLE_SIZE:
        sample_files = random.sample(all_labels, SAMPLE_SIZE)
        n_train = int(SAMPLE_SIZE * TRAIN_RATIO)
        s_train = sample_files[:n_train]
        s_val = sample_files[n_train:]

        for f in s_train:
            copy_image_and_label(f, "sample_500/train", f.parent)
        for f in s_val:
            copy_image_and_label(f, "sample_500/val", f.parent)
    else:
        print("Not enough data for 500-sample split")
        return

    # ====== STEP 3: Print summary ======
    print("\nDataset split summary:")
    for k, v in stats.items():
        print(f"- {k}: total={v['total']} train={v['train']} val={v['val']}")

    # ====== STEP 4: Generate YAMLs ======
    generate_yaml(
        yaml_path=OUTPUT_DIR / "data.yaml",
        path_root=str(OUTPUT_DIR),
        train_rel="train/images",
        val_rel="val/images"
    )
    generate_yaml(
        yaml_path=OUTPUT_DIR / "sample_500" / "data_sample.yaml",
        path_root=str(OUTPUT_DIR / "sample_500"),
        train_rel="train/images",
        val_rel="val/images"
    )


if __name__ == "__main__":
    split_dataset()
