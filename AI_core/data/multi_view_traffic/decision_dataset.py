import os
import shutil
import random
import zipapp

# Base path: Location about this script is located & Source YOLO label folders
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_PATH, "converted_yolo")
SOURCE_DIRS = {
    "drone": {
        "images": os.path.join(BASE_DIR, "drone_images"),
        "labels": os.path.join(BASE_DIR, "drone_labels"),
    },
    "infrastructure": {
        "images": os.path.join(BASE_DIR, "infrastructure_images"),
        "labels": os.path.join(BASE_DIR, "infrastructure_labels"),
    },
}
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
            for t in ["images", "labels"]:
                os.makedirs(os.path.join(OUTPUT_DIR, split, t, f"{sub}_{t}"), exist_ok=True)

def copy_pair(label_file, split, sub):
    """
    Copy label & image files if it exist
    """
    label_dst = os.path.join(OUTPUT_DIR, split, "labels", f"{sub}_labels", os.path.basename(label_file))
    shutil.copy2(label_file, label_dst)
    image_name = os.path.splitext(os.path.basename(label_file))[0] + ".jpg"
    image_src = os.path.join(SOURCE_DIRS[sub]["images"], image_name)
    if os.path.exists(image_src):
        image_dst = os.path.join(OUTPUT_DIR, split, "images", f"{sub}_images", image_name)
        shutil.copy2(image_src, image_dst)
    else:
        print(f"[WARNING] Missing image for label: {label_file}")


def main():
    prepare_output_folders()
    stats = {} 

    for sub, paths in SOURCE_DIRS.items():
        label_dir = paths["labels"]
        label_files = [os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith(".txt")]
        random.shuffle(label_files)

        n_total = len(label_files)
        n_train = round(n_total * train_ratio)
        train_files = label_files[:n_train]
        val_files = label_files[n_train:]

        for lf in train_files:
            copy_pair(lf, "train", sub)
        for lf in val_files:
            copy_pair(lf, "val", sub)

        stats[sub] = {
            "total": n_total,
            "train": len(train_files),
            "val": len(val_files),
        }
    print("=== Dataset Split Statistics ===")
    for sub, s in stats.items():
        print(f"\n{sub}:")
        print(f"  Total : {s['total']}")
        print(f"  Train : {s['train']} ({s['train']/s['total']:.2%})")
        print(f"  Val   : {s['val']} ({s['val']/s['total']:.2%})")



if __name__ == "__main__":
    main()
