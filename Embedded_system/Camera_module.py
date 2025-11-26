# Lấy hình ảnh làm đầu vào AI nhận diện
import time
from picamera2 import Picamera2
import threading

class CameraModule:
    def __init__(self, width=416, height=416, fps=15):
        self.picam2 = Picamera2()
        self.width = width
        self.height = height
        self.fps = fps

        video_config = self.picam2.create_video_configuration(main={"size": (self.width, self.height)})
        self.picam2.configure(video_config)
        self.picam2.start()
        self.frame_delay = 1.0 / self.fps

        # Lock để đảm bảo thread-safe
        self.lock = threading.Lock()

    def get_frame(self):
    
        # Trả về 1 frame từ camera, thread-safe
        with self.lock:
            start_time = time.time()
            frame = self.picam2.capture_array()
            elapsed = time.time() - start_time
            if elapsed < self.frame_delay:
                time.sleep(self.frame_delay - elapsed)
            return frame
        
    # camera chạy liên tục và lưu frame mới nhất 
    def camera_loop(self):
        while True:
            frame = self.get_frame()
            with self.lock:
                self.latest_frame = frame

    def stop(self):
        self.picam2.stop()
        print("[CameraModule] Camera stopped.")
