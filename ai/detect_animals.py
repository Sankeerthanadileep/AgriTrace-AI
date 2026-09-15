from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Detect objects in the farm video
results = model.predict(
    source="videos/farm_video.mp4",
    save=True,
    show=True
)

print("Detection completed!")