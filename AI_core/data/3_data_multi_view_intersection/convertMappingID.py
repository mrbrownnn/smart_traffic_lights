import os
from pathlib import Path

# ============================
# CONFIG
# ============================
DATA_ROOT = Path(__file__).parent.resolve()

# Old ordering from Roboflow
# ['bicycle', 'bus', 'car', 'motorbike', 'person']
ROBOFLOW_TO_TARGET = {
    0: 1,  # bicycle -> 1
    1: 2,  # bus -> 2
    2: 0,  # car -> 0
    3: 4,  # motorbike -> 4
    4: None,  # person -> remove
}

# ============================
# FUNCTION TO PROCESS LABEL FILE
# ============================

def process_label_file(label_path):
    with open(label_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        cls_id = int(parts[0])

        if cls_id not in ROBOFLOW_TO_TARGET:
            continue

        new_id = ROBOFLOW_TO_TARGET[cls_id]

        if new_id is None:
            continue   # remove person entirely

        # rewrite class id
        parts[0] = str(new_id)
        new_lines.append(" ".join(parts) + "\n")

    # Overwrite the file
    with open(label_path, "w") as f:
        f.writelines(new_lines)


# ============================
# MAIN
# ============================

if __name__ == "__main__":
    subsets = ["train", "valid", "test", "val"]  

    for subset in subsets:
        # Prefer labels/<subset>; fall back to <subset>/labels
        label_dir = DATA_ROOT / "labels" / subset
        if not label_dir.exists():
            alt_dir = DATA_ROOT / subset / "labels"
            label_dir = alt_dir if alt_dir.exists() else label_dir
        if not label_dir.exists():
            continue

        print(f"Processing: {label_dir}")

        for file in label_dir.glob("*.txt"):
            process_label_file(file)

    print("\nDONE — dataset cleaned + remapped successfully!")
