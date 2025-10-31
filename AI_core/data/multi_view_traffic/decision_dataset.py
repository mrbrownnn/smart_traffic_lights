"""
Split YOLO dataset (flat structure) into train/validation/test subsets.

This script:
1. Reads images (.jpg) and labels (.txt) stored together in each folder (e.g., 'drone/', 'infrastructure/').
2. Randomly splits each dataset into train (70%) and validation (30%).
3. Randomly selects 500 image–label pairs for testing.
4. Generates data.yaml (for training) and data_test.yaml (inside sample_2000/ for testing).
"""

import os
import shutil
import random
import yaml
from pathlib import Path


# ====================== CONFIGURATION ======================

BASE_PATH = Path(__file__).resolve().parent
BASE_DIR = BASE_PATH / "converted_yolo_2"     # Folder containing 'drone/' and 'infrastructure/'
OUTPUT_DIR = BASE_PATH / "split_yolo"         # Output folder after splitting

SOURCE_FOLDERS = ["drone", "infrastructure"]  # Dataset folders to process

TRAIN_RATIO = 0.7              # 70% train / 30% validation
SAMPLE_SIZE = 500             # Number of random samples for testing
CLASS_NAMES = ["car", "motorcycle", "bus", "truck"]

# ============================================================


def prepare_output_folders() -> None:
    """
    Reset and create the directory structure:
    split_yolo/
        ├── train/images/
        ├── train/labels/
        ├── val/images/
        ├── val/labels/
        ├── sample_500/images/
        └── sample_500/labels/
    """
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    for split in ["train", "val", "sample_500"]:
        for subfolder in ["images", "labels"]:
            os.makedirs(OUTPUT_DIR / split / subfolder, exist_ok=True)


def copy_image_and_label(label_path: Path, split_name: str, folder_root: Path) -> None:
    """
    Copy a label (.txt) and its matching image (.jpg) into the specified split folder.

    Args:
        label_path (Path): Path to the .txt label file.
        split_name (str): Split folder name ("train", "val", or "sample_500").
        folder_root (Path): Path where both .jpg and .txt files are stored.
    """
    label_name = label_path.name
    image_name = label_path.stem + ".jpg"

    # Source paths
    image_src = folder_root / image_name
    label_src = folder_root / label_name

    # Destination paths
    image_dst = OUTPUT_DIR / split_name / "images" / image_name
    label_dst = OUTPUT_DIR / split_name / "labels" / label_name

    # Copy files
    if label_src.exists():
        shutil.copy2(label_src, label_dst)
    if image_src.exists():
        shutil.copy2(image_src, image_dst)
    else:
        print(f"Warning: Missing image for label {label_name}")


def split_dataset() -> None:
    """
    Main function to split flat YOLO datasets and generate data.yaml / data_test.yaml.
    """
    prepare_output_folders()
    statistics = {}
    all_label_files = []

    # ========== STEP 1: Split train / val ==========
    for subset_name in SOURCE_FOLDERS:
        folder_path = BASE_DIR / subset_name
        label_files = [folder_path / f for f in os.listdir(folder_path) if f.endswith(".txt")]
        random.shuffle(label_files)

        total_files = len(label_files)
        train_count = int(total_files * TRAIN_RATIO)
        train_files = label_files[:train_count]
        val_files = label_files[train_count:]

        for label_file in train_files:
            copy_image_and_label(label_file, "train", folder_path)
        for label_file in val_files:
            copy_image_and_label(label_file, "val", folder_path)

        all_label_files.extend(label_files)
        statistics[subset_name] = {
            "total": total_files,
            "train": len(train_files),
            "val": len(val_files)
        }

    # ========== STEP 2: Create test samples (sample_500) ==========
    total_labels = len(all_label_files)
    sample_folder = OUTPUT_DIR / "sample_500"

    if total_labels >= SAMPLE_SIZE:
        sample_files = random.sample(all_label_files, SAMPLE_SIZE)
        for label_file in sample_files:
            parent_folder = label_file.parent
            copy_image_and_label(label_file, "sample_500", parent_folder)

        # Generate data_test.yaml inside sample_500/
        data_test_yaml = {
            "test": str(sample_folder / "images"),
            "nc": len(CLASS_NAMES),
            "names": CLASS_NAMES
        }
        yaml_path = sample_folder / "data_test.yaml"
        with open(yaml_path, "w", encoding="utf-8") as file:
            yaml.dump(data_test_yaml, file, allow_unicode=True)
        print(f"Created data_test.yaml inside {yaml_path.parent}")
    else:
        print(f"Warning: Not enough samples ({total_labels}) to create test dataset.")

    # ========== STEP 3: Print summary ==========
    print("\nDataset split summary:")
    for subset_name, stats in statistics.items():
        print(
            f"- {subset_name.capitalize()}: "
            f"Total={stats['total']} | Train={stats['train']} | Val={stats['val']}"
        )

    # ========== STEP 4: Generate main data.yaml ==========
    data_yaml = {
        "train": str(OUTPUT_DIR / "train" / "images"),
        "val": str(OUTPUT_DIR / "val" / "images"),
        "nc": len(CLASS_NAMES),
        "names": CLASS_NAMES
    }

    with open(OUTPUT_DIR / "data.yaml", "w", encoding="utf-8") as file:
        yaml.dump(data_yaml, file, allow_unicode=True)
    print(f"Created data.yaml inside {OUTPUT_DIR}")


if __name__ == "__main__":
    split_dataset()
