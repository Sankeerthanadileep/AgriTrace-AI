from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Track animals in the video
results = model.track(
    source="videos/farm_video.mp4",
    tracker="bytetrack.yaml",
    save=True,
    show=True,
    persist=True
)

print("Animal tracking completed!")