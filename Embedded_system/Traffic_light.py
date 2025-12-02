# Traffic_light.py mô phỏng và điều khiển đèn
import RPi.GPIO as GPIO
import time
import threading
import json
import paho.mqtt.client as mqtt

# -----------------------------
# Khai báo chân GPIO
# -----------------------------
# Cụm 1
LED1_GREEN, LED1_YELLOW, LED1_RED = 23, 12, 16
# Cụm 2
LED2_GREEN, LED2_YELLOW, LED2_RED = 26, 27, 22

# Trạng thái cho API
traffic_status_c1 = {"green_time": 17, "yellow_time": 3, "red_time": 20, "vehicles": None}
traffic_status_c2 = {"green_time": 17, "yellow_time": 3, "red_time": 20, "vehicles": None}

# Biến số xe từ MQTT
vehicles_c1 = None
vehicles_c2 = None

# Biến reset đèn
manual_reset_active = False

# Điều chỉnh thủ công từ API
manual_adjust_c1 = 0
manual_adjust_c2 = 0

# Khóa dùng chung
status_lock = threading.Lock()

# ----------------------------------------------------
# GPIO
# ----------------------------------------------------
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in [LED1_GREEN, LED1_YELLOW, LED1_RED,
                LED2_GREEN, LED2_YELLOW, LED2_RED]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

# ----------------------------------------------------
# MQTT HANDLER — thay thế hoàn toàn input_vehicles()
# ----------------------------------------------------
def on_mqtt_message(client, userdata, msg):
    global vehicles_c1, vehicles_c2
    try:
        data = json.loads(msg.payload.decode())

        v1 = data.get("c1")
        v2 = data.get("c2")

        with status_lock:
            vehicles_c1 = v1
            vehicles_c2 = v2

        print(f"[MQTT] cập nhật số xe: CỤM1 = {vehicles_c1}, CỤM2 = {vehicles_c2}")

    except Exception as e:
        print("MQTT error:", e)


def input_vehicles():

    client = mqtt.Client()
    client.on_message = on_mqtt_message

    client.connect("localhost", 1883, 60)
    client.subscribe("smart_traffic/vehicles")

    print("MQTT subscriber is running...")
    client.loop_forever()

# ----------------------------------------------------
# Điều chỉnh thời gian dựa trên số xe
# ----------------------------------------------------
def adjust_times_based_on_vehicles(c1_green, c1_red, c2_green, c2_red, v1, v2, threshold=10):
    if v1 is None or v2 is None:
        return c1_green, c1_red, c2_green, c2_red
    
    # Cả 2 đều không đông
    if v1 <= threshold and v2 <= threshold:
        return c1_green, c1_red, c2_green, c2_red
    
    # 1 bên đông
    if v1 > threshold and v2 <= threshold:
        return c1_green+3, max(2, c1_red-3), max(2, c2_green-3), c2_red+3
    if v2 > threshold and v1 <= threshold:
        return max(2, c1_green-3), c1_red+3, c2_green+3, max(2, c2_red-3)
    
    # Cả 2 đều đông
    if v1 > threshold and v2 > threshold:
        if v1 > v2:
            return c1_green+3, max(2, c1_red-3), max(2, c2_green-3), c2_red+3
        elif v2 > v1:
            return max(2, c1_green-3), c1_red+3, c2_green+3, max(2, c2_red-3)
        else:
            return c1_green, c1_red, c2_green, c2_red

# ----------------------------------------------------
# Chu kỳ chạy đèn
# ----------------------------------------------------
def run_traffic_cycle():
    global vehicles_c1, vehicles_c2

    c1_green, c1_yellow, c1_red = 17, 3, 20
    c2_green, c2_yellow, c2_red = 17, 3, 20

    while True:
        # reset mặc định
        c1_green, c1_yellow, c1_red = 17, 3, 20
        c2_green, c2_yellow, c2_red = 17, 3, 20

        with status_lock:
            if not manual_reset_active:

                c1_green += manual_adjust_c1
                c2_red   += manual_adjust_c1

                c2_green += manual_adjust_c2
                c1_red   += manual_adjust_c2

                c1_green, c1_red, c2_green, c2_red = adjust_times_based_on_vehicles(
                    c1_green, c1_red, c2_green, c2_red, vehicles_c1, vehicles_c2
                )

            # cập nhật API
            traffic_status_c1["green_time"] = c1_green
            traffic_status_c1["yellow_time"] = c1_yellow
            traffic_status_c1["red_time"] = c1_red
            traffic_status_c1["vehicles"] = vehicles_c1

            traffic_status_c2["green_time"] = c2_green
            traffic_status_c2["yellow_time"] = c2_yellow
            traffic_status_c2["red_time"] = c2_red
            traffic_status_c2["vehicles"] = vehicles_c2

        print(f"(CỤM 1: xanh = {c1_green}s ; đỏ = {c1_red}s)")
        print(f"(CỤM 2: xanh = {c2_green}s ; đỏ = {c2_red}s)")
        print("===============================")

        # Cụm 1 XANH — Cụm 2 ĐỎ
        GPIO.output(LED1_GREEN, 1)
        GPIO.output(LED2_RED, 1)
        time.sleep(c1_green)
        GPIO.output(LED1_GREEN, 0)
        GPIO.output(LED2_RED, 0)

        # Cụm 1 VÀNG — Cụm 2 ĐỎ
        GPIO.output(LED1_YELLOW, 1)
        GPIO.output(LED2_RED, 1)
        time.sleep(c1_yellow)
        GPIO.output(LED1_YELLOW, 0)
        GPIO.output(LED2_RED, 0)

        # Cụm 1 ĐỎ — Cụm 2 XANH
        GPIO.output(LED1_RED, 1)
        GPIO.output(LED2_GREEN, 1)
        time.sleep(c2_green)
        GPIO.output(LED1_RED, 0)
        GPIO.output(LED2_GREEN, 0)

        # Cụm 1 ĐỎ — Cụm 2 VÀNG
        GPIO.output(LED1_RED, 1)
        GPIO.output(LED2_YELLOW, 1)
        time.sleep(c2_yellow)
        GPIO.output(LED1_RED, 0)
        GPIO.output(LED2_YELLOW, 0)

# ----------------------------------------------------
# Cleanup
# ----------------------------------------------------
def cleanup():
    GPIO.cleanup()
    print("GPIO cleanup done.")
