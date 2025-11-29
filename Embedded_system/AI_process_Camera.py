# -----------------------------
# Import thư viện
# -----------------------------
import numpy as np
from PIL import Image, ImageDraw
from tflite_runtime.interpreter import Interpreter
import cv2
import time
import paho.mqtt.client as mqtt
import json
import os


# -----------------------------
# Bước 1: Cấu hình
"""
REVIEW CODE + REFACTOR:
- Chỉnh các siêu tham số conf_threshold, IoU để tránh vẽ bbox với nhiều hình ảnh rỗng
- Tùy chỉnh với detect_interval theo thời gian thực
- Vẽ bbox kèm label cùng conf_threshold + IoU_threshold để debug
"""
# -----------------------------
CONF_THRESHOLD = 0.08
IOU_THRESHOLD = 0.45
DETECT_INTERVAL = 10   # detect mỗi 10 giây
CLASS_NAMES = ["car", "bicycle", "bus", "truck", "motorbike"]

# Tạo thư mục lưu ảnh detect
os.makedirs("detect_frames", exist_ok=True)


# -----------------------------
# Bước 2: NMS
# -----------------------------
def nms(boxes, scores, iou_threshold):
    if len(boxes) == 0:
        return []

    boxes = boxes.astype(np.float32)
    scores = scores.astype(np.float32)
    selected = []
    idxs = np.argsort(scores)[::-1]

    while len(idxs) > 0:
        cur = idxs[0]
        selected.append(cur)

        cur_box = boxes[cur]
        rest = boxes[idxs[1:]]

        xx1 = np.maximum(cur_box[0], rest[:, 0])
        yy1 = np.maximum(cur_box[1], rest[:, 1])
        xx2 = np.minimum(cur_box[2], rest[:, 2])
        yy2 = np.minimum(cur_box[3], rest[:, 3])

        inter = np.maximum(0, xx2 - xx1) * np.maximum(0, yy2 - yy1)
        area1 = (cur_box[2] - cur_box[0]) * (cur_box[3] - cur_box[1])
        area2 = (rest[:, 2] - rest[:, 0]) * (rest[:, 3] - rest[:, 1])
        union = area1 + area2 - inter

        iou = inter / (union + 1e-6)
        idxs = idxs[1:][iou < iou_threshold]

    return selected

#debug: add IoU & Confident:
def calc_iou(boxA, boxB):
    x1 = max(boxA[0], boxB[0])
    y1 = max(boxA[1], boxB[1])
    x2 = min(boxA[2], boxB[2])
    y2 = min(boxA[3], boxB[3])

    inter = max(0, x2 - x1) * max(0, y2 - y1)
    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    union = areaA + areaB - inter

    return inter / (union + 1e-6)

# -----------------------------
# Bước 3: Load model
# -----------------------------
interpreter = Interpreter(model_path="best_float16.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_h = input_details[0]["shape"][1]
input_w = input_details[0]["shape"][2]

print("Model input:", input_details[0]["shape"])
print("Model output:", output_details[0]["shape"])


# -----------------------------
# Bước 4: Load camera Pi V2
# -----------------------------

# fix: dataset format: 640 x640 pixels
cap = cv2.VideoCapture(0)

# ĐẶT FPS CHO CAMERA (tùy module)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

if not cap.isOpened():
    print("Không mở được camera!")
    exit()

print("Bắt đầu xử lý camera realtime...\n")

last_detect_time = time.time()
detect_count = 0


# -----------------------------
# Bước 5: Loop realtime từ camera
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera lỗi, không lấy được frame!")
        continue

    # Chạy realtime đúng tốc độ camera
    time.sleep(1/30)

    now = time.time()

    # Chỉ detect mỗi 10 giây
    if now - last_detect_time < DETECT_INTERVAL:
        continue

    last_detect_time = now
    detect_count += 1
    print(f"=== DETECT LẦN {detect_count} ===")

    # Convert BGR → RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    orig_w, orig_h = img.size

    # Resize input model
    img_resized = img.resize((input_w, input_h))
    img_np = np.array(img_resized, dtype=np.float32) / 255.0
    img_np = np.expand_dims(img_np, 0)

    # -----------------------------
    # Bước 6: Inference
    # -----------------------------
    interpreter.set_tensor(input_details[0]['index'], img_np)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    output = np.squeeze(output)

    # tăng tín hiệu
    output[4, :] *= 50
    output[5:, :] *= 50

    output = output.T

    boxes_all, scores_all, class_all = [], [], []

    # -----------------------------
    # Bước 7: Decode output
    # -----------------------------
    for pred in output:
        x, y, w_box, h_box, obj_conf = pred[:5]
        class_prob = pred[5:]
        conf = obj_conf * np.max(class_prob)

        if conf < CONF_THRESHOLD:
            continue

        cls_id = np.argmax(class_prob)

        x1 = (x - w_box/2) * orig_w
        y1 = (y - h_box/2) * orig_h
        x2 = (x + w_box/2) * orig_w
        y2 = (y + h_box/2) * orig_h

        boxes_all.append([x1, y1, x2, y2])
        scores_all.append(conf)
        class_all.append(cls_id)

    if len(boxes_all) == 0:
        print("Không phát hiện được xe.")
        continue

    # -----------------------------
    # Bước 8: NMS
    # -----------------------------
    boxes_all = np.array(boxes_all)
    scores_all = np.array(scores_all)
    class_all = np.array(class_all)

    keep = nms(boxes_all, scores_all, IOU_THRESHOLD)

    # -----------------------------
    # Bước 9: Đếm xe trái/phải
    # -----------------------------
    left = 0
    right = 0
    mid_x = orig_w // 2

    draw = ImageDraw.Draw(img)
    draw.line([(mid_x, 0), (mid_x, orig_h)], fill="blue", width=3)

    for idx in keep:
        x1, y1, x2, y2 = boxes_all[idx]
        score = float(scores_all[idx])
        cls_id = int(class_all[idx])

        center = (x1 + x2) / 2
        if center < mid_x:
            left += 1
        else:
            right += 1

        # Debug IOU (so với bbox đầu tiên trong NMS)
        iou_debug = calc_iou(boxes_all[keep[0]], boxes_all[idx]) if len(keep) > 0 else 0

        # Bbox
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        # Label text
        label = f"{CLASS_NAMES[cls_id]} {score:.2f} IOU:{iou_debug:.2f}"
        text_w, text_h = draw.textsize(label)

        # Label background
        draw.rectangle([x1, y1 - text_h - 4, x1 + text_w + 4, y1], fill="red")
        draw.text((x1 + 2, y1 - text_h - 2), label, fill="white")

    print(f"LEFT = {left}  |  RIGHT = {right}")

    # -----------------------------
    # Bước 10: Lưu frame detect
    # -----------------------------
    save_path = f"detect_frames/frame_{detect_count}.jpg"
    img.save(save_path)
    print("Đã lưu ảnh detect:", save_path)

    # -----------------------------
    # Bước 11: Gửi MQTT
    # -----------------------------
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    payload = {"c1": left, "c2": right}
    client.publish("smart_traffic/vehicles", json.dumps(payload))

    client.disconnect()


cap.release()
print("\nHoàn thành!")
