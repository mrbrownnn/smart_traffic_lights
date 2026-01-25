# Models Directory

This directory contains trained YOLOv11 models optimized for traffic detection using Knowledge Distillation (KD) and model compression techniques.

## 📁 Directory Structure

```
models/
├── yolov11n_kd_customize/          # YOLOv11n with Knowledge Distillation
├── yolo11n_customize_quantize+KD/  # YOLOv11n with Quantization + KD
├── original_model_v11n.ipynb       # Training notebook for baseline model
├── v11_ghostconv_KD_quantization.ipynb  # Training notebook for optimized model
└── .gitignore
```

## 🎯 Model Variants

### 1. YOLOv11n with Knowledge Distillation (`yolov11n_kd_customize/`)

**Purpose**: Lightweight detection model trained using knowledge distillation from a larger teacher model.

**Key Features**:
- **Architecture**: YOLOv11n (nano) with custom GhostBlock modifications
- **Training Method**: Knowledge Distillation
- **Epochs**: 40
- **Batch Size**: 16
- **Image Size**: 640x640
- **Dataset**: YOLO MTID Motor dataset

**Training Configuration**:
- Optimizer: Auto
- Learning Rate: 0.01 (initial), 0.01 (final)
- Augmentations: HSV, translation, scaling, flipping, RandAugment
- Loss Weights: Box=7.5, Cls=0.5, DFL=1.5

**Contents**:
- Training/validation visualizations (batch images, PR curves, F1 curves)
- Confusion matrices (normalized and unnormalized)
- Training results (`results.csv`, `results.png`)
- Model weights in `weights/` subdirectory
- Training arguments (`args.yaml`)

---

### 2. YOLOv11n with Quantization + KD (`yolo11n_customize_quantize+KD/`)

**Purpose**: Further optimized model combining quantization and knowledge distillation for maximum efficiency.

**Key Features**:
- **Architecture**: Pruned YOLOv11n with quantization
- **Training Method**: Fine-tuning with KD on multi-view traffic data
- **Epochs**: 50
- **Batch Size**: 16
- **Image Size**: 640x640
- **Dataset**: Multi-view intersection dataset
- **Frozen Layers**: First 3 layers

**Training Configuration**:
- Optimizer: Auto
- Learning Rate: 1.0e-05 (initial), 0.01 (final)
- Cosine LR Scheduler: Enabled
- Cache: Enabled for faster training
- Augmentations: Same as base model

**Contents**:
- Training/validation visualizations
- Performance metrics and curves
- Model weights in `weights/` subdirectory
- Training arguments (`args.yaml`)

---

## 📊 Training Notebooks

### `original_model_v11n.ipynb`
Jupyter notebook for training the baseline YOLOv11n model without optimizations.

### `v11_ghostconv_KD_quantization.ipynb`
Comprehensive notebook implementing:
- GhostConv architecture modifications
- Knowledge distillation training pipeline
- Model quantization and pruning
- Performance evaluation

---

## 🚀 Usage

### Loading a Model

```python
from ultralytics import YOLO

# Load the KD-trained model
model = YOLO('models/yolov11n_kd_customize/weights/best.pt')

# Load the quantized model
model_quantized = YOLO('models/yolo11n_customize_quantize+KD/weights/best.pt')
```

### Running Inference

```python
# Run inference
results = model('path/to/image.jpg')

# Process results
for result in results:
    boxes = result.boxes  # Bounding boxes
    probs = result.probs  # Class probabilities
```

---

## 📈 Model Performance

Both models include comprehensive performance metrics:

- **Precision-Recall Curves** (`BoxPR_curve.png`)
- **F1 Score Curves** (`BoxF1_curve.png`)
- **Precision/Recall vs Confidence** (`BoxP_curve.png`, `BoxR_curve.png`)
- **Confusion Matrices** (normalized and unnormalized)
- **Training Progress** (`results.png`, `results.csv`)

---

## 🔧 Model Optimization Techniques

1. **Knowledge Distillation (KD)**
   - Teacher: YOLOv11l (large model)
   - Student: YOLOv11n (nano model)
   - Transfers knowledge from larger model to smaller one

2. **GhostConv Blocks**
   - Reduces computational cost
   - Maintains accuracy with fewer parameters

3. **Quantization**
   - Reduces model size
   - Faster inference on edge devices

4. **Pruning**
   - Removes redundant weights
   - Optimizes model architecture

---

## 📝 Notes

- All models are trained for traffic detection tasks
- Models are optimized for deployment on resource-constrained devices
- Training was performed on Google Colab with GPU acceleration
- Models support multi-view traffic intersection scenarios

---

## 🔗 Related Files

- Dataset preparation: `../data/
- Training scripts: Jupyter notebooks in this directory
- Configuration files: `args.yaml` in each model subdirectory
