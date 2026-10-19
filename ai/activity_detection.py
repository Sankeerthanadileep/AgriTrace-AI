from collections import defaultdict
from ultralytics import YOLO

VIDEO_PATH = "videos/farm_video.mp4"

model = YOLO("yolo11n.pt")

cow_activity = defaultdict(lambda: {
    "previous_center": None,
    "moving_frames": 0,
    "stationary_frames": 0
})

results = model.track(
    source=VIDEO_PATH,
    tracker="bytetrack.yaml",
    stream=True,
    persist=True,
    classes=[19]
)

for result in results:

    if result.boxes.id is None:
        continue

    track_ids = result.boxes.id.int().cpu().tolist()
    boxes = result.boxes.xyxy.cpu().tolist()

    for cow_id, box in zip(track_ids, boxes):

        x1, y1, x2, y2 = box

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        previous = cow_activity[cow_id]["previous_center"]

        if previous is not None:

            previous_x, previous_y = previous

            movement = (
                (center_x - previous_x) ** 2
                + (center_y - previous_y) ** 2
            ) ** 0.5

            if movement > 5:
                cow_activity[cow_id]["moving_frames"] += 1
            else:
                cow_activity[cow_id]["stationary_frames"] += 1

        cow_activity[cow_id]["previous_center"] = (
            center_x,
            center_y
        )


print("\n===== COW ACTIVITY & ALERTS =====")

for cow_id, data in cow_activity.items():

    moving = data["moving_frames"]
    stationary = data["stationary_frames"]

    total_frames = moving + stationary

    # Ignore very short tracks
    if total_frames < 50:
        continue

    movement_percentage = (moving / total_frames) * 100

    observed_seconds = total_frames / 25.0

    if movement_percentage >= 20:
        activity = "MOVING"
    else:
        activity = "STATIONARY"

    # Detect unusual inactivity
    if observed_seconds >= 20 and movement_percentage < 2:
        alert = "UNUSUAL INACTIVITY"
    else:
        alert = "NORMAL"

    print(f"\nCow ID: {cow_id}")
    print(f"Activity: {activity}")
    print(f"Movement: {movement_percentage:.1f}%")
    print(f"Observed: {observed_seconds:.1f} seconds")
    print(f"Alert: {alert}")