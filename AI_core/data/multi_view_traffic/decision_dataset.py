import os
import shutil
import random


# Base path: folder where this script is located & Source YOLO label folders
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_PATH, "converted_yolo")
SOURCE_DIRS = {
    "drone_labels": os.path.join(BASE_DIR, "drone_labels"),
    "infrastructure_labels": os.path.join(BASE_DIR, "infrastructure_labels"),
}

# Output folder for the split dataset
OUTPUT_DIR = os.path.join(BASE_PATH, "split_yolo")

train_ratio = 0.7  # 70% training
val_ratio = 0.3    # 30% validation

def prepare_output_folders():
    """
   The structure:
    split_yolo/
        train/labels/drone_labels/
        train/labels/infrastructure_labels/
        val/labels/drone_labels/
        val/labels/infrastructure_labels/
    """
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    for split in ["train", "val"]:
        for sub in SOURCE_DIRS.keys():
            os.makedirs(os.path.join(OUTPUT_DIR, split, "labels", sub), exist_ok=True)


def copy_files(files, split, subfolder):
    """
    Copy label files into the corresponding train/val folder,
    while keeping the subfolder (drone_labels / infrastructure_labels).
    """
    for f in files:
        filename = os.path.basename(f)
        dst = os.path.join(OUTPUT_DIR, split, "labels", subfolder, filename)
        shutil.copy2(f, dst)


def main():
    prepare_output_folders()

    stats = {} 

    for sub, src in SOURCE_DIRS.items():
        if not os.path.isdir(src):
            raise FileNotFoundError(f"Missing folder: {src}")
        files = [os.path.join(src, f) for f in os.listdir(src) if f.endswith(".txt")]
        random.shuffle(files)

        n_total = len(files)
        n_train = round(n_total * train_ratio)
        train_files = files[:n_train]
        val_files = files[n_train:]  

        copy_files(train_files, "train", sub)
        copy_files(val_files, "val", sub)

        stats[sub] = {
            "total": n_total,
            "train": len(train_files),
            "val": len(val_files),
            "train_ratio": len(train_files) / n_total if n_total > 0 else 0,
            "val_ratio": len(val_files) / n_total if n_total > 0 else 0,
        }

    print("=== Dataset Split Statistics ===")
    for sub, s in stats.items():
        print(f"\n{sub}:")
        print(f"  Total : {s['total']}")
        print(f"  Train : {s['train']} ({s['train_ratio']:.2%})")
        print(f"  Val   : {s['val']} ({s['val_ratio']:.2%})")


if __name__ == "__main__":
    main()
