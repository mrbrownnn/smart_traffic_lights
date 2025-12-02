import time
import cv2
import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter

# ==========================
# Load model
# ==========================
MODEL_PATH = "best_float16.tflite"
VIDEO_PATH = "VideoGiaoThong.mp4"

interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_h = input_details[0]["shape"][1]
input_w = input_details[0]["shape"][2]

print("Model input:", input_details[0]["shape"])
print("Model output:", output_details[0]["shape"])
print("Bắt đầu đo FPS (100 frame)...\n")

# ==========================
# Load video
# ==========================
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Không mở được video!")
    exit()

fps_list = []
MAX_FRAMES = 100
count = 0

# ==========================
# Loop đo FPS (100 frame)
# ==========================
while count < MAX_FRAMES:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1

    # Chuẩn bị ảnh input
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    img_resized = img.resize((input_w, input_h))
    img_np = np.array(img_resized, dtype=np.float32) / 255.0
    img_np = np.expand_dims(img_np, 0)

    interpreter.set_tensor(input_details[0]["index"], img_np)

    # Đo inference time
    t0 = time.time()
    interpreter.invoke()
    t1 = time.time()

    infer_time = t1 - t0
    fps_list.append(1.0 / infer_time)

# ==========================
# Kết quả cuối
# ==========================
cap.release()

if fps_list:
    avg_fps = sum(fps_list) / len(fps_list)
    print("===== KẾT QUẢ FPS =====")
    print(f"FPS trung bình: {avg_fps:.2f}")
    print(f"FPS cao nhất  : {max(fps_list):.2f}")
    print(f"FPS thấp nhất : {min(fps_list):.2f}")
    print(f"Tổng số frame đã đo: {count}")
else:
    print("Không tính được FPS")
