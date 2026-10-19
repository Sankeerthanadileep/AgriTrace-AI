import json
from datetime import datetime

RECORDS_PATH = "ai/animal_records.json"

with open(RECORDS_PATH, "r") as file:
    records = json.load(file)

alerts_created = 0

for animal_id, record in records.items():

    history = record.get("activity_history", {})

    observed = record.get(
        "observation",
        {}
    ).get(
        "observed_seconds",
        0
    )

    if observed < 10:
        continue

    stationary = history.get(
        "stationary_seconds",
        0
    )

    moving = history.get(
        "moving_seconds",
        0
    )

    total = (
        stationary
        + moving
        + history.get("feeding_seconds", 0)
        + history.get("drinking_seconds", 0)
        + history.get("resting_seconds", 0)
    )

    if total <= 0:
        continue

    stationary_percentage = (
        stationary / total
    ) * 100

    # Prototype behavioral deviation rule
    # This is NOT disease diagnosis.
    if stationary_percentage >= 80:

        message = (
            "Behavioral deviation detected. "
            "Animal showed prolonged stationary "
            "behavior during the observation period."
        )

        alert = {
            "type": "Behavioral Deviation",
            "message": message,
            "status": "Inspection recommended",
            "video_timestamp": "Observation period",
            "recorded_at": datetime.now().isoformat()
        }

        record["alerts"] = [alert]

        record["events"] = [{
            "event_type": "Behavioral Deviation",
            "observation": message,
            "status": "Inspection recommended",
            "video_timestamp": "Observation period",
            "recorded_at": datetime.now().isoformat()
        }]

        record["behavior_baseline"] = {
            "observed_seconds": round(
                observed,
                2
            ),
            "moving_percentage": round(
                (moving / total) * 100,
                2
            ),
            "stationary_percentage": round(
                stationary_percentage,
                2
            )
        }

        alerts_created += 1

    else:

        record["behavior_baseline"] = {
            "observed_seconds": round(
                observed,
                2
            ),
            "moving_percentage": round(
                (moving / total) * 100,
                2
            ),
            "stationary_percentage": round(
                stationary_percentage,
                2
            )
        }


with open(
    RECORDS_PATH,
    "w"
) as file:

    json.dump(
        records,
        file,
        indent=4
    )

print("======================================")
print("     AGRITRACE BEHAVIOR ANALYSIS")
print("======================================")
print()
print(
    f"Animals analyzed: {len(records)}"
)
print(
    f"Alerts created: {alerts_created}"
)
print()
print(
    "Behavioral analysis completed."
)
print(
    "Note: Alerts indicate behavioral "
    "deviation and recommend inspection."
)
print(
    "They do not represent disease diagnosis."
)