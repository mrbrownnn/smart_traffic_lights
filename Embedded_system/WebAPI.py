# WebAPI.py
from flask import Flask, Response, jsonify, request
import Traffic_light
import cv2

def create_app(camera_instance):
    app = Flask(__name__)

    # ----------------------------
    # API lấy trạng thái đèn
    # ----------------------------
    @app.route("/status", methods=["GET"])
    def get_traffic_status():
        status = {
            "traffic_light_1": {
                "green_time": Traffic_light.traffic_status_c1["green_time"],
                "yellow_time": Traffic_light.traffic_status_c1["yellow_time"],
                "red_time": Traffic_light.traffic_status_c1["red_time"],
                "vehicles": Traffic_light.traffic_status_c1["vehicles"]
            },
            "traffic_light_2": {
                "green_time": Traffic_light.traffic_status_c2["green_time"],
                "yellow_time": Traffic_light.traffic_status_c2["yellow_time"],
                "red_time": Traffic_light.traffic_status_c2["red_time"],
                "vehicles": Traffic_light.traffic_status_c2["vehicles"]
            }
        }
        return jsonify(status)

    # ----------------------------
    # API điều chỉnh đèn thủ công
    # ----------------------------
    @app.route("/manual_adjust/<int:cluster>/<int:seconds>", methods=["POST"])
    def manual_adjust(cluster, seconds):
        Traffic_light.manual_reset_active = False
        with Traffic_light.status_lock:
            if cluster == 1:
                Traffic_light.manual_adjust_c1 = seconds
            elif cluster == 2:
                Traffic_light.manual_adjust_c2 = seconds
        return {"status": "OK", "Cụm điều chỉnh": cluster, "Tăng số giây đèn xanh": seconds}
    
    # ----------------------------
    # API reset đèn về thời gian ban đầu
    # ----------------------------
    @app.route("/manual_reset", methods=["POST"])
    def manual_reset_all():
        with Traffic_light.status_lock:
            Traffic_light.manual_adjust_c1 = 0
            Traffic_light.manual_adjust_c2 = 0
            Traffic_light.manual_reset_active = True  # bật flag reset
        return {"status": "OK", "message": "Đã reset cả hai cụm về mặc định, tắt chức năng điều chỉnh đèn tự động"}
    
    # -----------------------------
    # API bật điều chỉnh đèn tự động
    # -----------------------------
    @app.route("/enable_ai", methods=["POST"])
    def enable_ai():
        Traffic_light.manual_reset_active = False
        return jsonify({"status": "OK", "message": "Chế độ điều chỉnh đèn tự động được bật"})


    # ----------------------------
    # API xem camera trực tiếp
    # ----------------------------
    @app.route("/camera")
    def camera_feed():
        def generate():
            while True:
                # Lấy frame mới nhất thread-safe
                with camera_instance.lock:
                    frame = camera_instance.latest_frame
                if frame is None:
                    continue
                # Encode frame thành JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                # Yield frame dạng MJPEG
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    return app
    
