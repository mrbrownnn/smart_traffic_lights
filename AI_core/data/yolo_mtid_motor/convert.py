"""
MTID Dataset + Motorbike Synthetic Data Merger
Fixed image search logic for nested folder structure
Fixed: idx variable and added val set augmentation
"""

from pathlib import Path
from tqdm import tqdm
import json
import os
import shutil
import random
import cv2
import numpy as np
import yaml


class MTIDMotorbikeMerger:
    COCO_TO_YOLO = {3: 0, 2: 1, 6: 2, 8: 3}  # car, bicycle, bus, truck
    CLASS_NAMES = ['car', 'bicycle', 'bus', 'truck', 'motorbike']
    MOTORBIKE_CLASS = 4
    
    DRONE_UNANNOTATED_RANGES = [(1, 31), (659, 659), (1001, 1318), (3301, 3327)]
    
    def __init__(self, mtid_root, motor_crops_dir, output_root, seed=42):
        self.mtid_root = Path(mtid_root)
        self.motor_crops_dir = Path(motor_crops_dir)
        self.output_root = Path(output_root)
        
        random.seed(seed)
        np.random.seed(seed)
        
        # Load motorbike crops
        self.motor_paths = list(self.motor_crops_dir.glob("*.jpg")) + \
                          list(self.motor_crops_dir.glob("*.png"))
        print(f"✓ Loaded {len(self.motor_paths)} motorbike crops")
        
        # Setup directories
        for d in ['images/train', 'images/val', 'labels/train', 'labels/val']:
            (self.output_root / d).mkdir(parents=True, exist_ok=True)
        
        # Cache for image search (speeds up repeated lookups)
        self.image_cache = {}
        
        self.stats = {
            'converted': 0,
            'augmented': 0,
            'motors_pasted': 0,
            'motors_overlap_rejected': 0
        }
    
    def build_image_index(self, img_root):
        """
        Build index of all images in folder (including subfolders)
        Returns: dict mapping filename -> full_path
        """
        print(f"[INFO] Building image index for: {img_root}")
        img_root_path = Path(img_root)
        
        if not img_root_path.exists():
            print(f"[ERROR] Path does not exist: {img_root}")
            return {}
        
        index = {}
        extensions = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
        
        # Search recursively
        for ext in extensions:
            for img_file in img_root_path.rglob(f"*{ext}"):
                if img_file.is_file():
                    # Use basename as key (might have duplicates!)
                    basename = img_file.name
                    if basename not in index:
                        index[basename] = img_file
                    else:
                        # Handle duplicate names (prefer shorter path = closer to root)
                        if len(str(img_file)) < len(str(index[basename])):
                            index[basename] = img_file
        
        print(f"[INFO] Found {len(index)} unique image files")
        if index:
            print(f"[INFO] Sample paths:")
            for i, (name, path) in enumerate(list(index.items())[:3]):
                print(f"  {i+1}. {name} -> {path}")
        
        return index
    
    def find_image_file(self, img_root, filename):
        """
        Smart image file search with caching
        """
        img_root_path = Path(img_root)
        
        # Build cache if not exists
        cache_key = str(img_root_path)
        if cache_key not in self.image_cache:
            self.image_cache[cache_key] = self.build_image_index(img_root)
        
        index = self.image_cache[cache_key]
        
        # Direct lookup
        if filename in index:
            return index[filename]
        
        # Try without extension
        stem = os.path.splitext(filename)[0]
        for key, path in index.items():
            if os.path.splitext(key)[0] == stem:
                return path
        
        # Try case-insensitive
        filename_lower = filename.lower()
        for key, path in index.items():
            if key.lower() == filename_lower:
                return path
        
        return None
    
    def is_frame_annotated(self, frame_num):
        for start, end in self.DRONE_UNANNOTATED_RANGES:
            if start <= frame_num <= end:
                return False
        return True
    
    def extract_frame_number(self, filename):
        try:
            parts = filename.split('_')
            if len(parts) >= 2:
                return int(parts[-1].split('.')[0])
        except:
            pass
        return -1
    
    def convert_bbox(self, bbox, img_w, img_h):
        """Convert COCO to YOLO with clipping"""
        x, y, bw, bh = bbox
        
        if bw <= 0 or bh <= 0:
            return None
        
        # Clip to boundaries
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(img_w, x + bw)
        y2 = min(img_h, y + bh)
        
        bw_clip = x2 - x1
        bh_clip = y2 - y1
        
        if bw_clip < 2 or bh_clip < 2:
            return None
        
        # Normalize
        x_c = (x1 + bw_clip / 2) / img_w
        y_c = (y1 + bh_clip / 2) / img_h
        w_n = bw_clip / img_w
        h_n = bh_clip / img_h
        
        if not (0 <= x_c <= 1 and 0 <= y_c <= 1 and 0 < w_n <= 1 and 0 < h_n <= 1):
            return None
        
        return (x_c, y_c, w_n, h_n)
    
    def calculate_iou(self, box1, box2):
        """Calculate IoU between two boxes (x_center, y_center, width, height)"""
        x1_min = box1[0] - box1[2] / 2
        y1_min = box1[1] - box1[3] / 2
        x1_max = box1[0] + box1[2] / 2
        y1_max = box1[1] + box1[3] / 2
        
        x2_min = box2[0] - box2[2] / 2
        y2_min = box2[1] - box2[3] / 2
        x2_max = box2[0] + box2[2] / 2
        y2_max = box2[1] + box2[3] / 2
        
        inter_xmin = max(x1_min, x2_min)
        inter_ymin = max(y1_min, y2_min)
        inter_xmax = min(x1_max, x2_max)
        inter_ymax = min(y1_max, y2_max)
        
        inter_w = max(0, inter_xmax - inter_xmin)
        inter_h = max(0, inter_ymax - inter_ymin)
        inter_area = inter_w * inter_h
        
        box1_area = box1[2] * box1[3]
        box2_area = box2[2] * box2[3]
        union_area = box1_area + box2_area - inter_area
        
        if union_area == 0:
            return 0
        
        return inter_area / union_area
    
    def parse_yolo_labels(self, label_path):
        """Parse existing YOLO labels"""
        if not label_path.exists():
            return []
        
        bboxes = []
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    cls, x_c, y_c, w, h = parts[:5]
                    bboxes.append((float(x_c), float(y_c), float(w), float(h)))
        return bboxes
    
    def paste_motorbike(self, bg, motor, x, y):
        """Paste with simple alpha blending"""
        h, w = motor.shape[:2]
        H, W = bg.shape[:2]
        
        if x < 0 or y < 0 or x >= W or y >= H:
            return None
        
        if x + w > W:
            w = W - x
            motor = motor[:, :w]
        if y + h > H:
            h = H - y
            motor = motor[:h, :]
        
        if w < 5 or h < 5:
            return None
        
        roi = bg[y:y+h, x:x+w]
        
        gray = cv2.cvtColor(motor, cv2.COLOR_BGR2GRAY)
        mask = (gray > 30).astype(np.float32)
        mask = np.expand_dims(mask, axis=2)
        
        blended = roi * (1 - mask) + motor * mask
        bg[y:y+h, x:x+w] = blended.astype(np.uint8)
        
        return (x, y, w, h)
    
    def augment_with_motorbike(self, img_path, label_path, aug_ratio=0.5):
        """Augment with overlap check"""
        if random.random() > aug_ratio or not self.motor_paths:
            return False
        
        bg = cv2.imread(str(img_path))
        if bg is None:
            return False
        
        H, W = bg.shape[:2]
        existing_bboxes = self.parse_yolo_labels(label_path)
        
        num_motors = random.randint(1, 2)
        new_labels = []
        
        for _ in range(num_motors):
            max_attempts = 10
            pasted = False
            
            for attempt in range(max_attempts):
                motor_path = random.choice(self.motor_paths)
                motor = cv2.imread(str(motor_path))
                if motor is None:
                    continue
                
                scale = random.uniform(0.3, 0.8)
                mh, mw = motor.shape[:2]
                new_w = int(mw * scale)
                new_h = int(mh * scale)
                
                if new_w < 5 or new_h < 5:
                    continue
                
                motor = cv2.resize(motor, (new_w, new_h))
                mh, mw = motor.shape[:2]
                
                max_x = W - mw
                max_y = H - mh
                
                if max_x < 0 or max_y < 0:
                    break
                
                x = random.randint(0, max_x)
                min_y = int(H * 0.5)
                if min_y > max_y:
                    min_y = 0
                y = random.randint(min_y, max_y)
                
                cx = (x + mw / 2) / W
                cy = (y + mh / 2) / H
                ww = mw / W
                hh = mh / H
                
                new_bbox = (cx, cy, ww, hh)
                
                max_iou = 0
                for exist_bbox in existing_bboxes:
                    iou = self.calculate_iou(new_bbox, exist_bbox)
                    max_iou = max(max_iou, iou)
                
                if max_iou < 0.3:
                    result = self.paste_motorbike(bg, motor, x, y)
                    if result is not None:
                        bx, by, bw, bh = result
                        
                        cx = (bx + bw / 2) / W
                        cy = (by + bh / 2) / H
                        ww = bw / W
                        hh = bh / H
                        
                        if 0 <= cx <= 1 and 0 <= cy <= 1 and 0 < ww <= 1 and 0 < hh <= 1:
                            new_labels.append(f"{self.MOTORBIKE_CLASS} {cx:.6f} {cy:.6f} {ww:.6f} {hh:.6f}")
                            existing_bboxes.append((cx, cy, ww, hh))
                            self.stats['motors_pasted'] += 1
                            pasted = True
                            break
                else:
                    self.stats['motors_overlap_rejected'] += 1
            
            if not pasted:
                break
        
        if new_labels:
            cv2.imwrite(str(img_path), bg)
            with open(label_path, 'a') as f:
                for label in new_labels:
                    f.write('\n' + label)
            self.stats['augmented'] += 1
            return True
        
        return False
    
    def convert_mtid_view(self, json_path, img_root, split, view):
        """Convert MTID view to YOLO format - FIXED IMAGE SEARCH"""
        print(f"\n{'='*70}")
        print(f"Converting {view.upper()} - {split.upper()}")
        print(f"{'='*70}")
        
        if not Path(json_path).exists():
            print(f"[ERROR] JSON not found: {json_path}")
            return []
        
        if not Path(img_root).exists():
            print(f"[ERROR] Image root not found: {img_root}")
            return []
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        print(f"\n[INFO] Total images in JSON: {len(data['images'])}")
        print(f"[INFO] Total annotations in JSON: {len(data['annotations'])}")
        
        if data['images']:
            print(f"\n[INFO] Sample filenames from JSON:")
            for i, img in enumerate(data['images'][:3]):
                print(f"  {i+1}. {img['file_name']}")
        
        image_map = {img['id']: img for img in data['images']}
        processed = {}
        
        debug = {
            'total_anns': len(data['annotations']),
            'skipped_category': 0,
            'skipped_no_img_info': 0,
            'skipped_unannotated_frame': 0,
            'skipped_img_not_exist': 0,
            'skipped_img_read_fail': 0,
            'skipped_size_mismatch': 0,
            'skipped_bbox_invalid': 0,
            'success': 0
        }
        
        for ann in tqdm(data['annotations'], desc=f"Converting {view} {split}", ncols=100):

            cat_id = ann['category_id']
            if cat_id not in self.COCO_TO_YOLO:
                debug['skipped_category'] += 1
                continue
            
            img_info = image_map.get(ann['image_id'])
            if img_info is None:
                debug['skipped_no_img_info'] += 1
                continue
            
            filename = os.path.basename(img_info['file_name'])
            
            if view == 'drone':
                frame_num = self.extract_frame_number(filename)
                if frame_num > 0 and not self.is_frame_annotated(frame_num):
                    debug['skipped_unannotated_frame'] += 1
                    continue
            
            src_img = self.find_image_file(img_root, filename)
            
            if src_img is None or not src_img.exists():
                debug['skipped_img_not_exist'] += 1
                if debug['skipped_img_not_exist'] <= 5:
                    print(f"[WARN] Image not found: {filename}")
                    print(f"       JSON path: {img_info['file_name']}")
                continue
            
            # Verify with OpenCV
            actual_img = cv2.imread(str(src_img))
            if actual_img is None:
                debug['skipped_img_read_fail'] += 1
                if debug['skipped_img_read_fail'] <= 3:
                    print(f"[WARN] Cannot read: {src_img}")
                continue
            
            actual_h, actual_w = actual_img.shape[:2]
            json_w, json_h = img_info['width'], img_info['height']
            
            if actual_w != json_w or actual_h != json_h:
                debug['skipped_size_mismatch'] += 1
                if debug['skipped_size_mismatch'] <= 3:
                    print(f"[WARN] Size mismatch {filename}: JSON({json_w}x{json_h}) vs Actual({actual_w}x{actual_h})")
                json_w, json_h = actual_w, actual_h
            
            result = self.convert_bbox(ann['bbox'], json_w, json_h)
            if result is None:
                debug['skipped_bbox_invalid'] += 1
                continue
            
            cls_id = self.COCO_TO_YOLO[cat_id]
            
            if filename not in processed:
                processed[filename] = {'src_path': src_img, 'annotations': []}
            processed[filename]['annotations'].append((cls_id, result[0], result[1], result[2], result[3]))
            debug['success'] += 1
            self.stats['converted'] += 1
        
        print(f"\n[DEBUG] Conversion breakdown:")
        print(f"  Total annotations:        {debug['total_anns']:6d}")
        print(f"  ✓ Successfully converted: {debug['success']:6d}")
        print(f"  ✗ Wrong category:         {debug['skipped_category']:6d}")
        print(f"  ✗ No image info:          {debug['skipped_no_img_info']:6d}")
        print(f"  ✗ Unannotated frame:      {debug['skipped_unannotated_frame']:6d}")
        print(f"  ✗ Image not exist:        {debug['skipped_img_not_exist']:6d}")
        print(f"  ✗ Image read fail:        {debug['skipped_img_read_fail']:6d}")
        print(f"  ✗ Size mismatch:          {debug['skipped_size_mismatch']:6d}")
        print(f"  ✗ Invalid bbox:           {debug['skipped_bbox_invalid']:6d}")
        print()
        
        if debug['success'] == 0:
            print("[ERROR] No annotations converted!")
            return []
 
        for filename, data in processed.items():
            file_stem = os.path.splitext(filename)[0]
            src_img_path = data['src_path']
            annotations = data['annotations']
            
            dst_img = self.output_root / 'images' / split / filename
            shutil.copy2(src_img_path, dst_img)
            
            label_file = self.output_root / 'labels' / split / f"{file_stem}.txt"
            with open(label_file, 'w') as f:
                for cls_id, x_c, y_c, w_n, h_n in annotations:
                    f.write(f"{cls_id} {x_c:.6f} {y_c:.6f} {w_n:.6f} {h_n:.6f}\n")
        
        print(f"Converted {len(processed)} images")
        return list(processed.keys())
    
    def stratified_split(self, train_ratio=0.8):
        """Split train/val by view (stratified)"""
        print(f"\n{'='*70}")
        print("Stratified train/val split")
        print(f"{'='*70}")
        
        train_img_dir = self.output_root / 'images' / 'train'
        train_lab_dir = self.output_root / 'labels' / 'train'
        val_img_dir = self.output_root / 'images' / 'val'
        val_lab_dir = self.output_root / 'labels' / 'val'
        
        all_images = list(train_img_dir.glob("*.jpg")) + list(train_img_dir.glob("*.png"))
        
        drone_imgs = [f for f in all_images if 'drone' in f.name.lower()]
        infra_imgs = [f for f in all_images if 'infra' in f.name.lower() or 'infrastructure' in f.name.lower()]
        
        print(f"Drone: {len(drone_imgs)} images")
        print(f"Infrastructure: {len(infra_imgs)} images")
        
        random.shuffle(drone_imgs)
        random.shuffle(infra_imgs)
        
        drone_split = int(len(drone_imgs) * train_ratio)
        infra_split = int(len(infra_imgs) * train_ratio)
        
        val_files = drone_imgs[drone_split:] + infra_imgs[infra_split:]
        
        for img_path in val_files:
            filename = img_path.name
            file_stem = img_path.stem
            
            shutil.move(str(img_path), str(val_img_dir / filename))
            
            label_file = train_lab_dir / f"{file_stem}.txt"
            if label_file.exists():
                shutil.move(str(label_file), str(val_lab_dir / f"{file_stem}.txt"))
        
        print(f" Moved {len(val_files)} images to val")
        print(f"  Train: {len(all_images) - len(val_files)}")
        print(f"  Val: {len(val_files)}")
    
    def augment_split(self, split='train', aug_ratio=0.5):
        """Augment only specified split - FIXED idx variable"""
        print(f"\n{'='*70}")
        print(f"Augmenting {split} set with motorbikes (ratio={aug_ratio})")
        print(f"{'='*70}")
        
        img_dir = self.output_root / 'images' / split
        lab_dir = self.output_root / 'labels' / split
        
        images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
        
        if not images:
            print(f"[WARNING] No images found in {split} set!")
            return
        
        # Reset stats for this split
        split_stats = {'augmented': 0, 'motors_pasted': 0, 'motors_overlap_rejected': 0}
        
        for img_path in tqdm(images, desc=f"Augment {split} set", ncols=100):
            file_stem = img_path.stem
            label_path = lab_dir / f"{file_stem}.txt"
            
            # Track stats before augmentation
            before_aug = self.stats['augmented']
            before_paste = self.stats['motors_pasted']
            before_reject = self.stats['motors_overlap_rejected']
            
            self.augment_with_motorbike(img_path, label_path, aug_ratio)
            
            # Update split-specific stats
            split_stats['augmented'] += (self.stats['augmented'] - before_aug)
            split_stats['motors_pasted'] += (self.stats['motors_pasted'] - before_paste)
            split_stats['motors_overlap_rejected'] += (self.stats['motors_overlap_rejected'] - before_reject)
        
        print(f"\n Augmented {split_stats['augmented']} images in {split} set")
        print(f"  Motors pasted: {split_stats['motors_pasted']}")
        print(f"  Rejected (overlap): {split_stats['motors_overlap_rejected']}")
    
    def create_yaml(self):
        config = {
            'path': str(self.output_root.absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'nc': len(self.CLASS_NAMES),
            'names': self.CLASS_NAMES
        }
        
        with open(self.output_root / 'data.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print(f"\n✓ Created data.yaml")


def main():
    MTID_ROOT = "E:/multi_2"
    MOTOR_CROPS = "E:/multi_2/motor"
    OUTPUT_ROOT = "E:/multi_2/yolo_mtid_motor"
    
    print("="*70)
    print("MTID + Motorbike Merger")
    print("="*70)
    merger = MTIDMotorbikeMerger(MTID_ROOT, MOTOR_CROPS, OUTPUT_ROOT)
    
    # Step 1: Convert both views to train
    merger.convert_mtid_view(
        json_path=f"{MTID_ROOT}/drone-mscoco.json",
        img_root=f"{MTID_ROOT}/Drone",
        split='train',
        view='drone'
    )
    
    merger.convert_mtid_view(
        json_path=f"{MTID_ROOT}/infrastructure-mscoco.json",
        img_root=f"{MTID_ROOT}/Infrastructure",
        split='train',
        view='infrastructure'
    )
    
    # Step 2: Split train/val (80/20)
    merger.stratified_split(train_ratio=0.8)
    
    # Step 3: Augment both train and val sets 
    merger.augment_split(split='train', aug_ratio=0.7)  # 70% of train images
    merger.augment_split(split='val', aug_ratio=0.3)    # 30% of val images (lower ratio)
    
    # Step 4: Create YAML config
    merger.create_yaml()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Converted: {merger.stats['converted']}")
    print(f"Total Augmented: {merger.stats['augmented']}")
    print(f"Total Motors pasted: {merger.stats['motors_pasted']}")
    print(f"Total Motors rejected (overlap): {merger.stats['motors_overlap_rejected']}")
    print("="*70)


if __name__ == "__main__":
    main()


"""
PS E:\multi_2> & C:\Users\admin\AppData\Local\Microsoft\WindowsApps\python3.13.exe e:/multi_2/convert.py
======================================================================
MTID + Motorbike Merger
======================================================================
✓ Loaded 941 motorbike crops

======================================================================
Converting DRONE - TRAIN
======================================================================

[INFO] Total images in JSON: 3335
[INFO] Total annotations in JSON: 50811

[INFO] Sample filenames from JSON:     
  1. Drone/0/seq3-drone_0000001.jpg    
  2. Drone/0/seq3-drone_0000002.jpg    
  3. Drone/0/seq3-drone_0000003.jpg
Converting drone train:   0%|                                             | 0/50811 [00:00<?, ?it/s][INFO] Building image index for: E:/multi_2/Drone
[INFO] Found 25177 unique image files
[INFO] Sample paths:
  1. seq3-drone_0000001.jpg -> E:\multi_2\Drone\0\seq3-drone_0000001.jpg
  2. seq3-drone_0000002.jpg -> E:\multi_2\Drone\0\seq3-drone_0000002.jpg
  3. seq3-drone_0000003.jpg -> E:\multi_2\Drone\0\seq3-drone_0000003.jpg
Converting drone train: 100%|████████████████████████████████| 50811/50811 [05:58<00:00, 141.88it/s]

[DEBUG] Conversion breakdown:
  Total annotations:         50811
  ✓ Successfully converted:  50489
  ✗ Wrong category:              0
  ✗ No image info:               0
  ✗ Unannotated frame:         320
  ✗ Image not exist:             0
  ✗ Image read fail:             0
  ✗ Size mismatch:               0
  ✗ Invalid bbox:                2

Converted 2957 images

======================================================================
Converting INFRASTRUCTURE - TRAIN
======================================================================

[INFO] Total images in JSON: 2441
[INFO] Total annotations in JSON: 14488

[INFO] Sample filenames from JSON:
  1. Infrastructure/0/seq3-infra_0000001.jpg
  2. Infrastructure/0/seq3-infra_0000002.jpg
  3. Infrastructure/0/seq3-infra_0000003.jpg
Converting infrastructure train:   0%|                                    | 0/14488 [00:00<?, ?it/s][INFO] Building image index for: E:/multi_2/Infrastructure
[INFO] Found 24951 unique image files
[INFO] Sample paths:
  1. seq3-infra_0000001.jpg -> E:\multi_2\Infrastructure\0\seq3-infra_0000001.jpg
  2. seq3-infra_0000002.jpg -> E:\multi_2\Infrastructure\0\seq3-infra_0000002.jpg
  3. seq3-infra_0000003.jpg -> E:\multi_2\Infrastructure\0\seq3-infra_0000003.jpg
Converting infrastructure train: 100%|███████████████████████| 14488/14488 [00:34<00:00, 416.09it/s]

[DEBUG] Conversion breakdown:
  Total annotations:         14488
  ✓ Successfully converted:  14486
  ✗ Wrong category:              0
  ✗ No image info:               0
  ✗ Unannotated frame:           0
  ✗ Image not exist:             0
  ✗ Image read fail:             0
  ✗ Size mismatch:               0
  ✗ Invalid bbox:                2

Converted 2439 images

======================================================================
Stratified train/val split
======================================================================
Drone: 2957 images
Infrastructure: 2439 images
✓ Moved 1080 images to val
  Train: 4316
  Val: 1080

======================================================================
Augmenting train set with motorbikes (ratio=0.7)
======================================================================
Augment train set: 100%|████████████████████████████████████████| 4316/4316 [08:30<00:00,  8.45it/s]

✓ Augmented 2996 images in train set
  Motors pasted: 4474
  Rejected (overlap): 1

======================================================================
Augmenting val set with motorbikes (ratio=0.3)
======================================================================
Augment val set: 100%|██████████████████████████████████████████| 2388/2388 [01:29<00:00, 26.63it/s]

✓ Augmented 660 images in val set
  Motors pasted: 976
  Rejected (overlap): 1

✓ Created data.yaml

======================================================================
SUMMARY
======================================================================
Converted: 64975
Total Augmented: 3656
Total Motors pasted: 5450
Total Motors rejected (overlap): 2
====================================
"""