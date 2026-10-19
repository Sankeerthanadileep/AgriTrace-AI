from collections import defaultdict
from ultralytics import YOLO

VIDEO_PATH = "videos/farm_video.mp4"
FPS = 25.0

# COCO class ID for cow
COW_CLASS_ID = 19

model = YOLO("yolo11n.pt")

cow_behavior = defaultdict(lambda: {
    "previous_center": None,
    "moving_frames": 0,
    "stationary_frames": 0
})

results = model.track(
    source=VIDEO_PATH,
    tracker="bytetrack.yaml",
    stream=True,
    persist=True,
    classes=[COW_CLASS_ID]
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

        previous = cow_behavior[cow_id]["previous_center"]

        if previous is not None:

            previous_x, previous_y = previous

            movement = (
                (center_x - previous_x) ** 2
                + (center_y - previous_y) ** 2
            ) ** 0.5

            if movement > 5:
                cow_behavior[cow_id]["moving_frames"] += 1
            else:
                cow_behavior[cow_id]["stationary_frames"] += 1

        cow_behavior[cow_id]["previous_center"] = (
            center_x,
            center_y
        )


import json

print("\n===== COW BEHAVIOR BASELINES =====")

baselines = {}

for cow_id, data in cow_behavior.items():

    moving = data["moving_frames"]
    stationary = data["stationary_frames"]

    total_frames = moving + stationary

    # Ignore very short observations
    if total_frames < 50:
        continue

    observed_seconds = total_frames / FPS

    movement_percentage = (moving / total_frames) * 100
    stationary_percentage = (stationary / total_frames) * 100

    baselines[str(cow_id)] = {
        "observed_seconds": round(observed_seconds, 2),
        "moving_percentage": round(movement_percentage, 2),
        "stationary_percentage": round(stationary_percentage, 2)
    }

    print(f"\nCow ID: {cow_id}")
    print(f"Observed: {observed_seconds:.1f} seconds")
    print(f"Moving: {movement_percentage:.1f}%")
    print(f"Stationary: {stationary_percentage:.1f}%")

# Save baselines
with open("ai/baselines.json", "w") as file:
    json.dump(baselines, file, indent=4)

print("\nBaseline data saved to ai/baselines.json")