from ultralytics import YOLO

model = YOLO("yolo8x-pose.pt")

results = model("https://ultralytics.com/images/bus.jpg")
keypoints = results[0].keypoints
print(keypoints.data)