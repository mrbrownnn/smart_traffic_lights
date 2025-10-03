# validate_coco.py
import json
from collections import Counter
from pathlib import Path

p = Path("infrastructure-mscoco.json")   
with open(p, "r", encoding="utf-8") as f:
    coco = json.load(f)

print("Top-level keys:", list(coco.keys()))
for k in ("images", "annotations", "categories"):
    v = coco.get(k)
    print(f"- {k}:", type(v), "len =" , (len(v) if isinstance(v, list) else "n/a"))

# show sample entries
if coco.get("images"):
    print("\nExample image entry:", coco["images"][0])
if coco.get("annotations"):
    print("Example annotation entry:", coco["annotations"][0])
if coco.get("categories"):
    print("Example category entry:", coco["categories"][0])

# quick bbox format heuristic
images_by_id = {img["id"]: img for img in coco.get("images", []) if "id" in img}
cnt = Counter({"xywh":0, "xyxy":0, "no_size":0, "weird":0})
for ann in coco.get("annotations", []):
    bbox = ann.get("bbox")
    if not bbox or len(bbox) < 4:
        cnt["weird"] += 1
        continue
    x, y, a2, a3 = bbox[:4]
    img = images_by_id.get(ann.get("image_id"))
    if not img or ("width" not in img or "height" not in img):
        cnt["no_size"] += 1
        continue
    W, H = img["width"], img["height"]
    # heuristic: if x + a2 <= W and y + a3 <= H → likely [x,y,w,h] (COCO)
    if (x + a2 <= W) and (y + a3 <= H):
        cnt["xywh"] += 1
    # else if a2 and a3 look like absolute coordinates inside image bounds → likely [x_min,y_min,x_max,y_max]
    elif (a2 <= W) and (a3 <= H) and (a2 > x) and (a3 > y):
        cnt["xyxy"] += 1
    else:
        cnt["weird"] += 1

print("\nBBox format heuristic counts:", dict(cnt))
print("\nInterpretation:")
print("- Nếu xywh >> xyxy  → file có khả năng là COCO (bbox = [x,y,w,h]).")
print("- Nếu xyxy >> xywh  → bbox có thể là [x_min,y_min,x_max,y_max] → CẦN convert sang [x,y,w,h].")
print("- Nếu no_size > 0      → một vài image entries thiếu width/height (convert tool có thể bỏ qua).")
print("- Nếu weird > 0        → có entries lạ, kiểm tra thủ công sample shown above.")
