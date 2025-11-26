# ==============================
# Import thư viện
# ==============================
import numpy as np
from PIL import Image, ImageDraw
from tflite_runtime.interpreter import Interpreter

# ==============================
# Cấu hình
# ==============================
CONF_THRESHOLD = 0.08
IOU_THRESHOLD = 0.45
CLASS_NAMES = ["car", "bicycle", "bus", "truck", "motorbike"]

# ==============================
# NMS
# ==============================
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

# ==============================
# Load model
# ==============================
interpreter = Interpreter(model_path="best_float16.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print("Input shape:", input_details[0]['shape'])
print("Output shape:", output_details[0]['shape'])

# ==============================
# Load ảnh
# ==============================
img = Image.open("test_image.jpg").convert("RGB")
orig_w, orig_h = img.size
input_h, input_w = input_details[0]['shape'][1], input_details[0]['shape'][2]
img_resized = img.resize((input_w, input_h))
img_np = np.array(img_resized, dtype=np.float32) / 255.0
img_np = np.expand_dims(img_np, 0)

# ==============================
# Inference
# ==============================
interpreter.set_tensor(input_details[0]['index'], img_np)
interpreter.invoke()
output = interpreter.get_tensor(output_details[0]['index'])  # [1,9,8400]
output = np.squeeze(output)  # [9,8400]

# ==============================
# Auto-rescale output
# ==============================
output[4,:] = output[4,:] * 50      # obj_conf
output[5:,:] = output[5:,:] * 50    # class_probs

# ==============================
# Decode output
# ==============================
output = output.T  # 8400 x 9
boxes_all, scores_all, class_all = [], [], []

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
    print("Không phát hiện được phương tiện nào.")
    exit()

# ==============================
# NMS
# ==============================
boxes_all = np.array(boxes_all)
scores_all = np.array(scores_all)
class_all = np.array(class_all)
keep = nms(boxes_all, scores_all, IOU_THRESHOLD)

# ==============================
# Hiển thị kết quả
# ==============================
draw = ImageDraw.Draw(img)
print("Kết quả nhận diện phương tiện:")
final_boxes = []

for i in keep:
    cls_name = CLASS_NAMES[class_all[i]]
    score = scores_all[i]
    box = boxes_all[i].astype(int)
    final_boxes.append((box, class_all[i], score))

    draw.rectangle(box.tolist(), outline="red", width=2)
    draw.text((box[0], box[1]-10), f"{cls_name} {score:.2f}", fill="red")

    print(f"- {cls_name} ({score:.2f})  box={box.tolist()}")

# ==============================
# Chia đôi ảnh – đếm xe bên trái / phải
# ==============================
mid_x = orig_w // 2
left_count = 0
right_count = 0

for box, cls_id, score in final_boxes:
    x1, y1, x2, y2 = box
    x_center = (x1 + x2) / 2

    if x_center < mid_x:
        left_count += 1
    else:
        right_count += 1

# Vẽ line chia đôi
draw.line([(mid_x, 0), (mid_x, orig_h)], fill="blue", width=3)

print("\n===== Thống kê theo nửa ảnh =====")
print(f"Xe bên TRÁI : {left_count}")
print(f"Xe bên PHẢI: {right_count}")
print(f"Tổng xe: {left_count + right_count}")

# ==============================
# Lưu ảnh
# ==============================
img.save("result_image.jpg")
print("\nĐã lưu ảnh kết quả: result_image.jpg")
# ==========================================
# MQTT PUBLISH – gửi số xe cho hệ thống đèn
# ==========================================
import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_TOPIC = "smart_traffic/vehicles"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

payload = {
    "c1": int(left_count),   # xe bên trái
    "c2": int(right_count)   # xe bên phải
}

client.publish(MQTT_TOPIC, json.dumps(payload))
print("Đã gửi MQTT:", payload)

client.disconnect()
