# 📘 Multi-View Traffic Intersection Dataset (YOLO Format)

## 🗂 Overview
The **Multi-View Traffic Intersection Dataset (MTID-YOLO)** is a curated and preprocessed version of the original **Multi-View Traffic Intersection Dataset (MTID)** presented by *Jensen et al., IEEE ITSC 2020*.  
This dataset has been **cleaned, filtered, and converted into YOLO-compatible format** for modern computer vision workflows (YOLOv8, YOLOv11, etc.), enabling efficient object detection, model training, and knowledge distillation experiments on real-world traffic scenes.

---

## 🧠 Original Source
**Paper:**  
> Jensen, M. B., Møgelmose, A., & Moeslund, T. B. (2020).  
> *Presenting the Multi-View Traffic Intersection Dataset (MTID): A Detailed Traffic-Surveillance Dataset.*  
> In *IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC)*, 2020. [DOI: 10.1109/ITSC45102.2020.9294694](https://doi.org/10.1109/ITSC45102.2020.9294694)

**Dataset Website:**  
Originally published by Aalborg University, containing synchronized videos from **multiple viewpoints** (infrastructure & drone) over the same urban intersection.

---

## 🧹 Preprocessing and Cleaning
The dataset was extensively refined for use in embedded AI and YOLO training pipelines.  
The following preprocessing steps were applied:

1. **Frame Filtering**
   - Removed non-annotated frames based on paper metadata and verified visually.  
   - Filtered frame ranges for drone footage such as `[1–31]`, `[659]`, `[1001–1318]`, `[3301–3327]`.
   - Excluded segments containing unannotated pedestrians or occluded views.

2. **Annotation Cleaning**
   - Removed frames with partial or missing bounding boxes.
   - Verified label consistency and corrected missing class mappings.
   - Excluded parked cars and static background objects.

3. **COCO → YOLOv8 Conversion**
   - Converted COCO annotations to YOLO format (`class_id x_center y_center width height`).
   - Normalized coordinates based on image width/height.
   - Re-mapped class IDs according to the subset of interest.

4. **Class Mapping**
   | Class | COCO ID | YOLO ID |
   |--------|----------|----------|
   | Car | 2 | 0 |
   | Motorcycle | 3 | 1 |
   | Bus | 5 | 2 |
   | Truck (Lorry) | 7 | 3 |

5. **Dataset Structure**
   - Unified both *drone* and *infrastructure* datasets.
   - Removed duplicates and ensured one label per image.

6. **Data Split**
   - Automatically split into **train (70%)**, **validation (30%)**, and a **sample_500** subset for testing/distillation.
   - Script: [`split_yolo_dataset_flat_sample500.py`](./split_yolo_dataset_flat_sample500.py)

---

## 📁 Final Directory Structure
```
converted_yolo_2/
├── drone/
│   ├── seq3-drone_0000001.jpg
│   ├── seq3-drone_0000001.txt
│   └── ...
├── infrastructure/
│   ├── seq2-infra_0000001.jpg
│   ├── seq2-infra_0000001.txt
│   └── ...
split_yolo/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
├── sample_500/
│   ├── images/
│   ├── labels/
│   └── data_test.yaml
└── data.yaml
```

---

## 📜 YAML Configuration
**`data.yaml`**
```yaml
train: split_yolo/train/images
val: split_yolo/val/images
nc: 4
names: ['car', 'motorcycle', 'bus', 'truck']
```

**`sample_500/data_test.yaml`**
```yaml
test: split_yolo/sample_500/images
nc: 4
names: ['car', 'motorcycle', 'bus', 'truck']
```

---

## ⚙️ Usage
You can train or evaluate YOLOv8/YOLOv11 models directly using:
```bash
yolo detect train data=data.yaml model=yolov8n.pt epochs=100 imgsz=416
```

To evaluate or distill knowledge on the test subset:
```bash
yolo detect val data=split_yolo/sample_500/data_test.yaml model=best.pt
```

---

## 🚦 Dataset Summary

| Attribute | Description |
|------------|-------------|
| Total images | ~6,000 annotated (after filtering) |
| Views | Drone view, Infrastructure view |
| Resolution | 1920×1080 (original), 416×416 (training) |
| Frame rate | 30 FPS (video source) |
| Annotated classes | Car, Motorcycle, Bus, Truck |
| Split ratio | 70% train / 30% val / 500 test samples |
| Format | YOLOv8/YOLOv11 compatible |
| Annotation type | Bounding boxes (normalized) |

---

## 💾 Scripts Used
| Script | Purpose |
|--------|----------|
| `convert_coco_to_yolo.py` | Convert original COCO JSON annotations to YOLO format |
| `split_yolo_dataset_flat_sample500.py` | Split dataset into train/val/test sets and generate YAML configs |
| `data_cleanup.py` *(optional)* | Remove duplicates, invalid labels, or missing pairs |

---

## 🔐 Notes
- This dataset version is tailored for **AI embedded systems** (e.g., Raspberry Pi 4 inference).  
- All annotations and image pairs were manually validated for consistency.  
- For efficient deployment, training resolution typically ranges from **320×320 to 416×416**.

---

## 🏷 Citation
If using this dataset, please cite both the **original authors** and the **converted version**:
```text
Jensen, M. B., Møgelmose, A., & Moeslund, T. B. (2020).
Presenting the Multi-View Traffic Intersection Dataset (MTID): A Detailed Traffic-Surveillance Dataset.
IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC), 2020.
DOI: 10.1109/ITSC45102.2020.9294694
```

and optionally reference:

Thanh Pham et al. (2025). 
MTID-YOLO Clean Dataset Conversion for Embedded AI Traffic Control Systems.
Posts and Telecommunications Institute of Technology (PTIT), Viet Nam.
```

---

## 🧩 License
This dataset inherits the original license from MTID (Aalborg University, Denmark).  
Converted labels and split configuration scripts are distributed under the **MIT License**.

---

## 🧠 Acknowledgment
Special thanks to:
- **Aalborg University / ITSC 2020 authors** for providing the base dataset.


Have a nice day 😊