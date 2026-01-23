from ultralytics import YOLO

model = YOLO("yolov8x.pt")

results = model("https://ultralytics.com/images/bus.jpg")
boxes = results[0].boxes
for box in boxes:
    print(box.data)
print(results[0].names)