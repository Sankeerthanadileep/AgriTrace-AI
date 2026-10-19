import json
from datetime import datetime


def create_animal_record(cow_id, baseline):

    record = {
        "animal_id": cow_id,

        "identity": {
            "tracking_id": cow_id,
            "permanent_id": None
        },

        "behavior_baseline": {
            "observed_seconds": baseline["observed_seconds"],
            "moving_percentage": baseline["moving_percentage"],
            "stationary_percentage": baseline["stationary_percentage"]
        },

        "current_behavior": {
            "activity": None,
            "moving_percentage": None,
            "stationary_percentage": None
        },

        "activity_history": {
            "moving_seconds": 0,
            "stationary_seconds": 0,
            "feeding_seconds": 0,
            "drinking_seconds": 0,
            "resting_seconds": 0,
            "herd_interaction_seconds": 0,
            "separated_seconds": 0
        },

        "events": [],

        "alerts": [],

        "farm_records": {
            "breed": None,
            "age": None,
            "weight": None,
            "vaccinations": [],
            "breeding_records": [],
            "milk_production": [],
            "veterinary_records": []
        },

        "last_updated": datetime.now().isoformat()
    }

    return record


# Load behavioral baselines
with open("ai/baselines.json", "r") as file:
    baselines = json.load(file)


animal_records = {}

for cow_id, baseline in baselines.items():

    animal_records[cow_id] = create_animal_record(
        cow_id,
        baseline
    )


# Save records
with open("ai/animal_records.json", "w") as file:
    json.dump(animal_records, file, indent=4)


print(
    f"Created records for "
    f"{len(animal_records)} tracked animals."
)

print("Animal records saved to ai/animal_records.json")