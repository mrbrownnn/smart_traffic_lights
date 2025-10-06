Smart Traffic Light Edge-AI (Raspberry Pi 4)

Hệ thống điều khiển đèn giao thông chạy AI trực tiếp trên Raspberry Pi 4 (Edge), không phụ thuộc cloud inference.
Pipeline đầy đủ: dataset → train → prune → quantize (INT8) → export TFLite → deploy trên Pi → logic điều khiển đèn + dashboard realtime.

🔥 Tính năng chính

Nhận diện phương tiện realtime bằng YOLOv8n-Lite, input 480×480 (trade-off tối ưu cho Pi 4).

Tối ưu model: Ghost/DWConv backbone (tùy chọn), Structured Pruning (≤65%) + TFLite INT8.

Logic đèn thông minh: đếm mật độ theo hướng, ưu tiên làn đông, hysteresis chống nhấp nháy.

Triển khai Edge: Pi 4 CPU-only, multi-thread (Capture / Inference / Logic / MQTT).

Kết nối IoT: publish MQTT trạng thái & thống kê, sync Firebase (tuỳ chọn).

Dashboard: hiển thị camera, đếm xe, trạng thái đèn theo thời gian thực.
