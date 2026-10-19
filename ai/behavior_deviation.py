import json
from collections import defaultdict
from ultralytics import YOLO

from video_timestamp import frame_to_timestamp


VIDEO_PATH = "videos/farm_video.mp4"

FPS = 25.0
COW_CLASS_ID = 19
DEVIATION_THRESHOLD = 10.0


# Load behavioral baselines
with open("ai/baselines.json", "r") as file:
    baselines = json.load(file)

# Load animal records
with open("ai/animal_records.json", "r") as file:
    animal_records = json.load(file)


model = YOLO("yolo11n.pt")


cow_behavior = defaultdict(lambda: {
    "previous_center": None,
    "moving_frames": 0,
    "stationary_frames": 0,
    "deviation_frame": None
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

        if cow_id not in baselines:
            continue

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


print("\n===== BEHAVIOR ANALYSIS =====")


for cow_id, data in cow_behavior.items():

    moving = data["moving_frames"]
    stationary = data["stationary_frames"]

    total_frames = moving + stationary

    if total_frames < 50:
        continue

    current_movement = (moving / total_frames) * 100

    normal_movement = baselines[cow_id]["moving_percentage"]

    difference = abs(
        current_movement - normal_movement
    )

    print(f"\nCow ID: {cow_id}")
    print(f"Baseline movement: {normal_movement:.1f}%")
    print(f"Current movement: {current_movement:.1f}%")
    print(f"Difference: {difference:.1f}%")


    if difference >= DEVIATION_THRESHOLD:

        # Calculate approximate timestamp
        timestamp = frame_to_timestamp(
            frame_number,
            FPS
        )

        observation = (
            "Behavior differs significantly from "
            "the individual behavioral baseline."
        )

        event = {
            "event_type": "Behavioral Deviation",
            "observation": observation,
            "status": "Inspection recommended",
            "video_timestamp": timestamp,
            "frame_number": frame_number
        }

        animal_records[cow_id]["events"].append(event)

        animal_records[cow_id]["alerts"].append({
            "type": "Behavioral Deviation",
            "message": observation,
            "video_timestamp": timestamp,
            "frame_number": frame_number
        })

        print("⚠️ BEHAVIORAL DEVIATION DETECTED")
        print(f"Video timestamp: {timestamp}")
        print(f"Frame: {frame_number}")

    else:

        print("✓ Behavior within individual baseline")


# Save updated records
with open("ai/animal_records.json", "w") as file:
    json.dump(animal_records, file, indent=4)


print("\nAnimal records updated successfully.")