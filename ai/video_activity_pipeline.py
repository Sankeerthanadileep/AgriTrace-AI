from collections import defaultdict
from ultralytics import YOLO

from activity_classifier import classify_movement
from activity_tracker import add_activity, get_activity_summary
import json


VIDEO_PATH = "videos/farm_video.mp4"

FPS = 25.0
COW_CLASS_ID = 19
MOVEMENT_THRESHOLD = 5


model = YOLO("yolo11n.pt")

cow_state = defaultdict(lambda: {
    "previous_center": None
})


results = model.track(
    source=VIDEO_PATH,
    tracker="bytetrack.yaml",
    stream=True,
    persist=True,
    classes=[COW_CLASS_ID]
)


for frame_number, result in enumerate(results):

    if result.boxes.id is None:
        continue

    track_ids = result.boxes.id.int().cpu().tolist()
    boxes = result.boxes.xyxy.cpu().tolist()

    for cow_id, box in zip(track_ids, boxes):

        cow_id = str(cow_id)

        x1, y1, x2, y2 = box

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        previous = cow_state[cow_id]["previous_center"]

        if previous is None:

            cow_state[cow_id]["previous_center"] = (
                center_x,
                center_y
            )

            continue

        previous_x, previous_y = previous

        movement = (
            (center_x - previous_x) ** 2
            + (center_y - previous_y) ** 2
        ) ** 0.5

        if movement > MOVEMENT_THRESHOLD:
            activity = classify_movement(100)
        else:
            activity = classify_movement(0)

        add_activity(cow_id, activity)

        cow_state[cow_id]["previous_center"] = (
            center_x,
            center_y
        )


print("\n===== VIDEO ACTIVITY SUMMARY =====")

for cow_id in cow_state:

    summary = get_activity_summary(cow_id)

    print(f"\nCow ID: {cow_id}")

    for activity, seconds in summary.items():
        print(f"{activity}: {seconds} seconds")


# Save activity data to animal records
with open("ai/animal_records.json", "r") as file:
    animal_records = json.load(file)


for cow_id in cow_state:

    if cow_id not in animal_records:
        continue

    summary = get_activity_summary(cow_id)

    animal_records[cow_id]["activity_history"] = summary

    total_moving = summary["moving_seconds"]
    total_stationary = summary["stationary_seconds"]

    total = total_moving + total_stationary

    if total > 0:

        movement_percentage = (
            total_moving / total
        ) * 100

        stationary_percentage = (
            total_stationary / total
        ) * 100

        animal_records[cow_id]["current_behavior"] = {
            "activity": (
                "moving"
                if movement_percentage >= 20
                else "stationary"
            ),
            "moving_percentage": round(
                movement_percentage, 2
            ),
            "stationary_percentage": round(
                stationary_percentage, 2
            )
        }


with open("ai/animal_records.json", "w") as file:
    json.dump(
        animal_records,
        file,
        indent=4
    )


print("\nAnimal records updated with video activity.")