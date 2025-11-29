import os
from pathlib import Path
from collections import defaultdict

# ============================
# CONFIG
# ============================
DATA_ROOT = Path(__file__).parent.resolve()

# Class names (adjust according to your dataset)
CLASS_NAMES = {
    0: "car",
    1: "bicycle", 
    2: "bus",
    4: "motorbike"
}

# ============================
# FUNCTION TO COUNT CLASSES
# ============================

def count_classes_in_file(label_path):
    """Count class occurrences in a single label file."""
    class_counts = defaultdict(int)
    
    try:
        with open(label_path, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 5:
                continue
            
            try:
                cls_id = int(parts[0])
                class_counts[cls_id] += 1
            except ValueError:
                continue
                
    except Exception as e:
        print(f"Error reading {label_path}: {e}")
    
    return class_counts


# ============================
# MAIN
# ============================

if __name__ == "__main__":
    subsets = ["train", "valid", "test", "val"]
    
    # Store stats for each subset
    subset_stats = {}
    total_stats = defaultdict(int)
    
    print("=" * 70)
    print("CLASS DISTRIBUTION ANALYSIS")
    print("=" * 70)
    
    for subset in subsets:
        # Try different possible label directory structures
        label_dir = DATA_ROOT / "labels" / subset
        if not label_dir.exists():
            alt_dir = DATA_ROOT / subset / "labels"
            label_dir = alt_dir if alt_dir.exists() else label_dir
        
        if not label_dir.exists():
            continue
        
        # Count classes in this subset
        subset_counts = defaultdict(int)
        file_count = 0
        
        for file in label_dir.glob("*.txt"):
            file_count += 1
            file_counts = count_classes_in_file(file)
            
            for cls_id, count in file_counts.items():
                subset_counts[cls_id] += count
                total_stats[cls_id] += count
        
        subset_stats[subset] = {
            'counts': subset_counts,
            'files': file_count,
            'total_annotations': sum(subset_counts.values())
        }
    
    # ============================
    # DISPLAY RESULTS
    # ============================
    
    # Per-subset breakdown
    for subset, stats in subset_stats.items():
        print(f"\n📁 {subset.upper()}")
        print(f"   Files: {stats['files']}")
        print(f"   Total annotations: {stats['total_annotations']}")
        print(f"   Classes:")
        
        for cls_id in sorted(stats['counts'].keys()):
            count = stats['counts'][cls_id]
            class_name = CLASS_NAMES.get(cls_id, f"Unknown-{cls_id}")
            percentage = (count / stats['total_annotations'] * 100) if stats['total_annotations'] > 0 else 0
            print(f"      [{cls_id}] {class_name:15s}: {count:6d} ({percentage:5.2f}%)")
    
    # Overall statistics
    print("\n" + "=" * 70)
    print("📊 OVERALL STATISTICS")
    print("=" * 70)
    
    total_annotations = sum(total_stats.values())
    total_files = sum(s['files'] for s in subset_stats.values())
    
    print(f"\nTotal files: {total_files}")
    print(f"Total annotations: {total_annotations}")
    print(f"\nClass distribution:")
    
    for cls_id in sorted(total_stats.keys()):
        count = total_stats[cls_id]
        class_name = CLASS_NAMES.get(cls_id, f"Unknown-{cls_id}")
        percentage = (count / total_annotations * 100) if total_annotations > 0 else 0
        
        # Visual bar
        bar_length = int(percentage / 2)  # Scale to 50 chars max
        bar = "█" * bar_length
        
        print(f"[{cls_id}] {class_name:15s}: {count:6d} ({percentage:5.2f}%) {bar}")
    
    # Average annotations per file
    if total_files > 0:
        avg_annotations = total_annotations / total_files
        print(f"\nAverage annotations per file: {avg_annotations:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)