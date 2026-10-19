import json
from datetime import datetime

from video_timestamp import frame_to_timestamp


# Load existing animal records
with open("ai/animal_records.json", "r") as file:
    animal_records = json.load(file)


def add_event(
    animal_id,
    event_type,
    observation,
    status,
    frame_number,
    fps
):
    animal_id = str(animal_id)

    if animal_id not in animal_records:
        print(f"Animal {animal_id} not found.")
        return

    timestamp = frame_to_timestamp(frame_number, fps)

    event = {
        "event_type": event_type,
        "observation": observation,
        "status": status,
        "video_timestamp": timestamp,
        "frame_number": frame_number,
        "recorded_at": datetime.now().isoformat()
    }

    animal_records[animal_id]["events"].append(event)

    if status == "Inspection recommended":

        animal_records[animal_id]["alerts"].append({
            "type": event_type,
            "message": observation,
            "video_timestamp": timestamp,
            "frame_number": frame_number,
            "recorded_at": datetime.now().isoformat()
        })


# -------------------------------------------------
# TEST EVENT
# -------------------------------------------------

add_event(
    animal_id="1",
    event_type="Behavioral Deviation",
    observation=(
        "Behavior differs significantly from "
        "the individual behavioral baseline."
    ),
    status="Inspection recommended",
    frame_number=625,
    fps=25.0
)


# Save updated records
with open("ai/animal_records.json", "w") as file:
    json.dump(animal_records, file, indent=4)


print("Event recorded successfully.")
print("Video timestamp:", "00:00:25")
print("Animal records updated.")