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
# Cấu hình
# -----------------------------
CONF_THRESHOLD = 0.08  
IOU_THRESHOLD = 0.5
DETECT_INTERVAL = 5   # detect mỗi 5 giây
CLASS_NAMES = ["car", "bicycle", "bus", "truck", "motorbike"]
# Tạo thư mục lưu ảnh detect
os.makedirs("detect_frames", exist_ok=True)

# -----------------------------
# NMS
# -----------------------------
def nms(boxes, scores, iou_threshold):
    if len(boxes) == 0:
        return []

    boxes = boxes.astype(np.float32)
    scores = scores.astype(np.float32)
    selected = []

    idxs = np.argsort(scores)[::-1]  # sort từ cao xuống

    while len(idxs) > 0:
        cur = idxs[0]
        selected.append(cur)

        cur_box = boxes[cur]
        rest = boxes[idxs[1:]]

        xx1 = np.maximum(cur_box[0], rest[:,0])
        yy1 = np.maximum(cur_box[1], rest[:,1])
        xx2 = np.minimum(cur_box[2], rest[:,2])
        yy2 = np.minimum(cur_box[3], rest[:,3])

        inter = np.maximum(0, xx2 - xx1) * np.maximum(0, yy2 - yy1)
        area1 = (cur_box[2]-cur_box[0])*(cur_box[3]-cur_box[1])
        area2 = (rest[:,2]-rest[:,0])*(rest[:,3]-rest[:,1])
        union = area1 + area2 - inter

        iou = inter / (union + 1e-6)
        idxs = idxs[1:][iou < iou_threshold]

    return selected


# -----------------------------
# Load model
# -----------------------------
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "best_float16.tflite"
)

interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_h = input_details[0]["shape"][1]
input_w = input_details[0]["shape"][2]

print("Model input:", input_details[0]["shape"])
print("Model output:", output_details[0]["shape"])


# -----------------------------
# Load video
# -----------------------------
VIDEO_PATH = os.path.join(
    os.path.dirname(__file__),
    "VideoGiaoThong2.mp4"
)
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Không mở được video!")
    exit()

print("Bắt đầu xử lý video...\n")

last_detect_time = time.time()
detect_count = 0   # đếm lần detect để lưu ảnh


# -----------------------------
# Loop xử lý video
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("Video đã hết!")
        break

    # tốc độ xem video bình thường (30 fps)
    time.sleep(1/30)

    now = time.time()

    # Chỉ detect mỗi 5s
    if now - last_detect_time < DETECT_INTERVAL:
        continue

    last_detect_time = now
    detect_count += 1
    print(f"=== DETECT LẦN {detect_count} ===")

    # Convert BGR → PIL RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    orig_w, orig_h = img.size

    # Resize ảnh input model
    img_resized = img.resize((input_w, input_h))
    img_np = np.array(img_resized, dtype=np.float32) / 255.0
    img_np = np.expand_dims(img_np, 0)

    # -----------------------------
    # Inference
    # -----------------------------
    interpreter.set_tensor(input_details[0]['index'], img_np)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    output = np.squeeze(output)  # [8400, 9]
    output = output.T  # [8400, 9]

    boxes_all, scores_all, class_all = [], [], []

    # -----------------------------
    # Decode output
    # -----------------------------
    for pred in output:
        x, y, w_box, h_box = pred[:4]
        class_scores = pred[4:]

        cls_id = int(np.argmax(class_scores))
        conf = class_scores[cls_id]

        if conf < CONF_THRESHOLD:
            continue

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
    # NMS
    # -----------------------------
    boxes_all = np.array(boxes_all)
    scores_all = np.array(scores_all)
    class_all = np.array(class_all)

    keep = nms(boxes_all, scores_all, IOU_THRESHOLD)

    # -----------------------------
    # Đếm xe trái / phải
    # -----------------------------
    left = 0
    right = 0
    mid_x = orig_w // 2

    draw = ImageDraw.Draw(img)

    # Vẽ line chia đôi
    draw.line([(mid_x, 0), (mid_x, orig_h)], fill="blue", width=3)

    for i in keep:
        x1, y1, x2, y2 = boxes_all[i]
        center = (x1 + x2) / 2

        if center < mid_x:
            left += 1
        else:
            right += 1

        # Vẽ bounding box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

    print(f"LEFT = {left}  |  RIGHT = {right}")

    # -----------------------------
    # Lưu ảnh detect
    # -----------------------------
    save_path = f"detect_frames/frame_{detect_count}.jpg"
    img.save(save_path)
    print("Đã lưu ảnh detect:", save_path)

    # -----------------------------
    # Gửi MQTT
    # -----------------------------
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    payload = {"c1": left, "c2": right}
    client.publish("smart_traffic/vehicles", json.dumps(payload))

    client.disconnect()


cap.release()
print("\nHoàn thành!")
