import time
import numpy as np
from tflite_runtime.interpreter import Interpreter

""": WARNING:
- tflite runtime package only works with python 3.7 to 3.10
- tflite runtime only works with cpu (ARM/Intel)
- for GPU support, use tensorflow package instead
"""
MODEL_PATH ="C:\\Users\\admin\\Desktop\\project_local_backup\\AI_core\\distillation_models\\yolo11n_ghost_distilled\\weights\\best_saved_model\\best_float16.tflite"
interpreter = Interpreter()
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

inp = np.random.randint(0, 255, input_details[0]['shape'], dtype=np.uint8)

# warmup
for _ in range(5):
    interpreter.set_tensor(input_details[0]['index'], inp)
    interpreter.invoke()

# measure
times = []
for _ in range(50):
    t1 = time.perf_counter()
    interpreter.invoke()
    t2 = time.perf_counter()
    times.append((t2 - t1) * 1000)

print("Avg latency:", sum(times)/len(times), "ms")
print("p50:", sorted(times)[25], "ms")
print("p90:", sorted(times)[45], "ms")
