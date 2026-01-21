# 🚦 Smart Traffic Light System with Edge AI (Raspberry Pi 4)

An **Edge-AI–based smart traffic light control system** running **entirely on Raspberry Pi 4**, without relying on cloud inference.  
The system performs **real-time vehicle detection, traffic density estimation, and adaptive signal control** directly at the edge.

This project demonstrates a **full end-to-end Edge-AI pipeline**, from data preparation to on-device deployment, targeting **resource-constrained embedded systems**.

---

## 🔧 System Overview

### 📌 End-to-End Pipeline

```
Dataset → Model Customization → Training → Knowledge Distillation
→ Fine-tuning → INT8 Quantization → TFLite Export
→ Edge Deployment (Raspberry Pi 4) → Traffic Logic → Realtime Dashboard
```

- Inference runs **fully on-device (CPU-only)**
- Designed for **low-power embedded hardware**
- Focused on **real-world deployability**, not just offline accuracy

---

## 🔥 Key Features

### 🚗 Real-time Vehicle Detection
- **YOLOv11n-Lite (customized)** object detection model
- Input resolution: **416 × 416**
- Optimized trade-off between **accuracy, latency, and CPU load** on Raspberry Pi 4
- Supports multiple vehicle classes:
  - Car
  - Bicycle
  - Motorbike
  - Bus
  - Truck

---

### ⚙️ Model Optimization for Edge AI
- Lightweight backbone options:
  - **Custom Architecture with GhostConv & C3k2 Block**
  - **Knowledge distillation**
  - **Finetune with Multi-view-traffic-Intersection**
  - **Quantization**
  - 
- **INT8 Quantization** using **TensorFlow Lite Runtime**
- CPU-friendly inference with **minimal accuracy degradation**
- Designed for stable real-time performance on Raspberry Pi 4

---

### 🚦 Intelligent Traffic Light Control Logic
- Real-time vehicle counting per direction
- **Density-aware signal scheduling**:
  - Green time dynamically allocated to congested lanes
- **Hysteresis mechanism** to prevent rapid signal flickering
- Rule-based logic designed for **stability and safety**

---

### 🧠 Edge Deployment Architecture
- Runs on **Raspberry Pi 4 (CPU-only)**
- Multi-threaded execution model:
  - Video Capture Thread  
  - AI Inference Thread  
  - Traffic Logic Thread  
  - Communication / MQTT Thread  
- Ensures **stable real-time operation** under limited hardware resources

---

### 🌐 IoT Connectivity
- Publishes traffic statistics and signal states via **MQTT**
- Optional synchronization with **Firebase** for cloud monitoring
- Modular communication layer, easy to extend and integrate

---

### 📊 Real-time Dashboard
- Live camera stream
- Vehicle counts per lane
- Current traffic light states
- Real-time system statistics

---

## 🎯 Project Goals
- Demonstrate **practical Edge-AI deployment** on low-power hardware
- Achieve **real-time traffic analysis without cloud dependency**
- Balance **model accuracy vs. inference speed vs. hardware constraints**
- Serve as a **research-oriented undergraduate capstone project**

---

## 🛠 Hardware & Software

### Hardware
- Raspberry Pi 4  
- Pi Camera Module v2  
- GPIO-controlled traffic lights (LEDs)

### Software
- Python (for data cleaning & Embeded Systems)
- Jupyter Notebook (for architecture,training and finetune model)
- YOLOv11n (customized)  
- TensorFlow Lite (INT8, FP16)  
- OpenCV  
- MQTT  
- Nextjs (for web & dardboard)
- Firebase (optional)

---

## 📜 License & Usage

This repository is provided **for academic and demonstration purposes only**.

Access to and reuse of the source code (including training scripts, optimization pipelines, and deployment code) **require explicit permission from the author**.

📩 **For any requests to use the source code, please contact:**  
**Thanh Pham Van** (repository owner)

Unauthorized commercial use, redistribution, or modification of this project is **not permitted** without prior consent.

---

## 🙏 Acknowledgements

Special thanks to the following projects and datasets that made this work possible:

- **Ultralytics** – YOLO framework and training utilities  
- **MTID Dataset** – Multi-View Traffic Intersection Dataset  
- **VisDrone Dataset** – Drone-based traffic and vehicle annotations  
- **Roboflow Dataset** – Dataset management and preprocessing tools  
- **Google Colab** - Cloud environment for training AI

---
