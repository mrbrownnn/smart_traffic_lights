#!/usr/bin/env python3
"""
Script phát hiện và đếm phương tiện sử dụng YOLOv8n
Hỗ trợ đếm theo vùng (region) và theo đường (line)
"""

import cv2
import argparse
from pathlib import Path
from ultralytics import YOLO
from ultralytics.solutions import ObjectCounter, RegionCounter
from ultralytics.utils import ASSETS

def vehicle_detection_simple(source, model_path="yolov8n.pt", device="cpu", show=True, save=False):
    """
    Phát hiện phương tiện đơn giản với YOLOv8n
    
    Args:
        source: Đường dẫn video hoặc 0 cho webcam
        model_path: Đường dẫn model YOLOv8n
        device: Thiết bị xử lý (cpu, 0, 1, ...)
        show: Hiển thị kết quả
        save: Lưu kết quả
    """
    
    # Load model
    model = YOLO(model_path)
    
    # Vehicle classes trong COCO dataset
    vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
    
    # Chạy detection
    results = model.predict(
        source=source,
        device=device,
        classes=vehicle_classes,
        conf=0.5,
        show=show,
        save=save,
        verbose=True
    )
    
    return results

def vehicle_counting_line(source, model_path="yolov8n.pt", device="cpu", show=True, save=False):
    """
    Đếm phương tiện qua một đường thẳng
    
    Args:
        source: Đường dẫn video hoặc 0 cho webcam
        model_path: Đường dẫn model YOLOv8n
        device: Thiết bị xử lý
        show: Hiển thị kết quả
        save: Lưu kết quả
    """
    
    # Load model
    model = YOLO(model_path)
    
    # Vehicle classes
    vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
    
    # Điểm đường đếm (có thể thay đổi theo video)
    line_points = [(100, 400), (800, 400)]  # Đường ngang giữa màn hình
    
    # Khởi tạo ObjectCounter
    counter = ObjectCounter(
        show=show,
        region=line_points,
        model=model_path,
        line_width=2,
        classes=vehicle_classes
    )
    
    # Xử lý video
    cap = cv2.VideoCapture(source)
    assert cap.isOpened(), f"Không thể mở video: {source}"
    
    # Lấy thông tin video
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    
    # Video writer nếu cần lưu
    if save:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter("vehicle_counting_output.avi", fourcc, fps, (w, h))
    
    print("🚗 Bắt đầu đếm phương tiện...")
    print("📊 Nhấn 'q' để thoát")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        # Đếm phương tiện
        results = counter(frame)
        
        # Hiển thị thông tin
        print(f"Vào: {counter.in_count}, Ra: {counter.out_count}, Tổng: {counter.in_count + counter.out_count}")
        
        # Lưu frame nếu cần
        if save:
            video_writer.write(results.plot_im)
        
        # Thoát nếu nhấn 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    if save:
        video_writer.release()
    
    print(f"\n📊 Kết quả cuối cùng:")
    print(f"   Phương tiện vào: {counter.in_count}")
    print(f"   Phương tiện ra: {counter.out_count}")
    print(f"   Tổng: {counter.in_count + counter.out_count}")

def vehicle_counting_region(source, model_path="yolov8n.pt", device="cpu", show=True, save=False):
    """
    Đếm phương tiện trong vùng xác định
    
    Args:
        source: Đường dẫn video hoặc 0 cho webcam
        model_path: Đường dẫn model YOLOv8n
        device: Thiết bị xử lý
        show: Hiển thị kết quả
        save: Lưu kết quả
    """
    
    # Load model
    model = YOLO(model_path)
    
    # Vehicle classes
    vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
    
    # Khởi tạo RegionCounter
    counter = RegionCounter(
        show=show,
        model=model_path,
        line_width=2,
        classes=vehicle_classes
    )
    
    # Thêm vùng đếm (có thể thay đổi theo video)
    # Vùng 1: Góc trái trên
    counter.add_region(
        name="Zone1",
        polygon=[(100, 100), (400, 100), (400, 300), (100, 300)],
        color=(255, 0, 0),  # Màu đỏ
        text_color=(255, 255, 255)  # Màu trắng
    )
    
    # Vùng 2: Góc phải dưới
    counter.add_region(
        name="Zone2", 
        polygon=[(500, 300), (800, 300), (800, 500), (500, 500)],
        color=(0, 255, 0),  # Màu xanh lá
        text_color=(255, 255, 255)  # Màu trắng
    )
    
    # Xử lý video
    cap = cv2.VideoCapture(source)
    assert cap.isOpened(), f"Không thể mở video: {source}"
    
    # Lấy thông tin video
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    
    # Video writer nếu cần lưu
    if save:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter("vehicle_region_counting_output.avi", fourcc, fps, (w, h))
    
    print("🚗 Bắt đầu đếm phương tiện theo vùng...")
    print("📊 Nhấn 'q' để thoát")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        # Đếm phương tiện trong các vùng
        results = counter(frame)
        
        # Hiển thị thông tin
        print(f"Zone1: {counter.region_counts.get('Zone1', 0)}, Zone2: {counter.region_counts.get('Zone2', 0)}")
        
        # Lưu frame nếu cần
        if save:
            video_writer.write(results.plot_im)
        
        # Thoát nếu nhấn 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    if save:
        video_writer.release()
    
    print(f"\n📊 Kết quả cuối cùng:")
    for zone_name, count in counter.region_counts.items():
        print(f"   {zone_name}: {count} phương tiện")

def main():
    parser = argparse.ArgumentParser(description="Phát hiện và đếm phương tiện với YOLOv8n")
    parser.add_argument("--source", type=str, default="0", help="Đường dẫn video hoặc 0 cho webcam")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Đường dẫn model YOLOv8n")
    parser.add_argument("--device", type=str, default="cpu", help="Thiết bị xử lý (cpu, 0, 1, ...)")
    parser.add_argument("--mode", type=str, choices=["detect", "line", "region"], default="detect", 
                       help="Chế độ: detect (phát hiện), line (đếm theo đường), region (đếm theo vùng)")
    parser.add_argument("--show", action="store_true", help="Hiển thị kết quả")
    parser.add_argument("--save", action="store_true", help="Lưu kết quả")
    
    args = parser.parse_args()
    
    print("🚗 YOLOv8n Vehicle Detection & Counting")
    print("=" * 50)
    print(f"📹 Nguồn: {args.source}")
    print(f"🤖 Model: {args.model}")
    print(f"💻 Thiết bị: {args.device}")
    print(f"🎯 Chế độ: {args.mode}")
    print("=" * 50)
    
    if args.mode == "detect":
        vehicle_detection_simple(args.source, args.model, args.device, args.show, args.save)
    elif args.mode == "line":
        vehicle_counting_line(args.source, args.model, args.device, args.show, args.save)
    elif args.mode == "region":
        vehicle_counting_region(args.source, args.model, args.device, args.show, args.save)

if __name__ == "__main__":
    main()
