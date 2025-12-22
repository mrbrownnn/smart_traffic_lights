🚦 Smart Traffic Light System with Edge AI (Raspberry Pi 4)
An Edge-AI–based smart traffic light control system running entirely on Raspberry Pi 4, without relying on cloud inference.
The system performs real-time vehicle detection, traffic density estimation, and adaptive signal control directly at the edge.
This project demonstrates a full end-to-end Edge-AI pipeline, from data preparation to on-device deployment.
🔧 System Overview
Pipeline:
Dataset-> Customize Models → Training → KD -> Finetune → INT8 Quantization → TFLite Export
→ Edge Deployment (Raspberry Pi 4) → Traffic Logic → Realtime Dashboard
Inference runs fully on-device (CPU-only)
Designed for resource-constrained embedded systems
Focused on real-world deployability, not just offline accuracy
🔥 Key Features
🚗 Real-time Vehicle Detection
YOLOv11n-Lite customize object detection
Input resolution: 480×480
Optimized trade-off between accuracy, latency, and CPU load on Raspberry Pi 4
Detects multiple vehicle classes (e.g., car, motorbike, bus, truck)
⚙️ Model Optimization for Edge AI
Lightweight backbone options:
GhostConv
Depthwise Separable Convolution (DWConv)
INT8 Quantization with TensorFlow Lite
CPU-friendly inference with minimal accuracy degradation
🚦 Intelligent Traffic Light Control Logic
Vehicle counting per direction in real time
Density-aware signal timing:
Green time dynamically allocated to congested lanes
Hysteresis mechanism to prevent rapid signal flickering
Rule-based control designed for stability and safety
🧠 Edge Deployment Architecture
Runs on Raspberry Pi 4 (CPU-only)
Multi-threaded design:
Video Capture Thread
AI Inference Thread
Traffic Logic Thread
Communication / MQTT Thread
Ensures stable real-time performance under limited hardware resources
🌐 IoT Connectivity
Publishes traffic statistics and signal states via MQTT
Optional synchronization with Firebase for cloud monitoring
Modular communication layer, easy to extend
📊 Real-time Dashboard
Live camera stream
Vehicle counts per lane
Current traffic light states
Real-time system statistics
🎯 Project Goals
Demonstrate practical Edge-AI deployment on low-power hardware
Achieve real-time traffic analysis without cloud dependency
Balance model accuracy vs. inference speed vs. hardware constraints
Serve as a research-oriented undergraduate capstone project
🛠 Hardware & Software
Hardware:Raspberry Pi 4,Pi Camera Module v2, GPIO-controlled traffic lights (LEDs)
Software: Python,YOLOv11n baseline, TensorFlow Lite (INT8), OpenCV, MQTT,Firebase (optional)
📜 License & Usage
This repository is provided for academic and demonstration purposes only.
Source code access and reuse (including training scripts, optimization pipelines, and deployment code)
require explicit permission from the author.
📩 For any requests to use the source code, please contact:
mrbrownn (own this reposity)
Unauthorized commercial use, redistribution, or modification of this project is not permitted without prior consent.
🙏 Acknowledgements
Special thanks to the following projects and datasets that made this work possible:
- Ultralytics – YOLO framework and training utilities
- MTID Dataset – Multi-View Traffic Intersection Dataset
- VisDrone Dataset – Drone-based traffic and vehicle annotations
- Roboflow Dataset – Dataset management and preprocessing tools
🔎 Note
This project focuses on Edge-AI deployment and system integration.
All third-party frameworks and datasets are used in compliance with their respective licenses.
