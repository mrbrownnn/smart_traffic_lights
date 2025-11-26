# Main.py vận hành hệ thống
import threading
import Traffic_light
from WebAPI import create_app
from Camera_module import CameraModule

# -----------------------------
# Thread chạy camera
# -----------------------------
camera = CameraModule()
web_app = create_app(camera)
camera_thread = threading.Thread(target=camera.camera_loop, daemon=True)
camera_thread.start()

# -----------------------------
# Thread nhận số xe từ AI qua MQTT
# -----------------------------
mqtt_thread = threading.Thread(target=Traffic_light.input_vehicles, daemon=True)
mqtt_thread.start()

# -----------------------------
# Thread chạy đèn giao thông
# -----------------------------
def run_traffic():
    Traffic_light.setup_gpio()
    try:
        Traffic_light.run_traffic_cycle()
    except KeyboardInterrupt:
        Traffic_light.cleanup()

led_thread = threading.Thread(target=run_traffic, daemon=True)
led_thread.start()

# -----------------------------
# Thread chạy Flask API
# -----------------------------
def run_api():
    web_app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

api_thread = threading.Thread(target=run_api, daemon=True)
api_thread.start()

# Giữ main thread
try:
    while True:
        pass
except KeyboardInterrupt:
    Traffic_light.cleanup()
    print("Chương trình kết thúc.")
