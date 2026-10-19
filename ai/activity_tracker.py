from collections import defaultdict
import json
from datetime import datetime


# ======================================
# VIDEO SETTINGS
# ======================================

FPS = 30.0


# ======================================
# ACTIVITY DATA
# ======================================

activity_data = defaultdict(
    lambda: {
        "moving_frames": 0,
        "stationary_frames": 0,
        "feeding_frames": 0,
        "drinking_frames": 0,
        "resting_frames": 0,
        "herd_interaction_frames": 0,
        "separated_frames": 0
    }
)


# ======================================
# ADD ACTIVITY
# ======================================

def add_activity(cow_id, activity):

    if activity == "moving":

        activity_data[cow_id][
            "moving_frames"
        ] += 1

    elif activity == "stationary":

        activity_data[cow_id][
            "stationary_frames"
        ] += 1

    elif activity == "feeding":

        activity_data[cow_id][
            "feeding_frames"
        ] += 1

    elif activity == "drinking":

        activity_data[cow_id][
            "drinking_frames"
        ] += 1

    elif activity == "resting":

        activity_data[cow_id][
            "resting_frames"
        ] += 1

    elif activity == "herd_interaction":

        activity_data[cow_id][
            "herd_interaction_frames"
        ] += 1

    elif activity == "separated":

        activity_data[cow_id][
            "separated_frames"
        ] += 1


# ======================================
# ACTIVITY SUMMARY
# ======================================

def get_activity_summary(cow_id):

    data = activity_data[cow_id]

    return {

        "moving_seconds":
            round(
                data["moving_frames"] / FPS,
                2
            ),

        "stationary_seconds":
            round(
                data["stationary_frames"] / FPS,
                2
            ),

        "feeding_seconds":
            round(
                data["feeding_frames"] / FPS,
                2
            ),

        "drinking_seconds":
            round(
                data["drinking_frames"] / FPS,
                2
            ),

        "resting_seconds":
            round(
                data["resting_frames"] / FPS,
                2
            ),

        "herd_interaction_seconds":
            round(
                data["herd_interaction_frames"] / FPS,
                2
            ),

        "separated_seconds":
            round(
                data["separated_frames"] / FPS,
                2
            )
    }


# ======================================
# UPDATE ANIMAL RECORD
# ======================================

def update_animal_record(
    cow_id,
    summary
):

    with open(
        "ai/animal_records.json",
        "r"
    ) as file:

        animal_records = json.load(file)


    cow_id = str(cow_id)


    if cow_id not in animal_records:

        print(
            f"Cow {cow_id} not found "
            "in animal records."
        )

        return


    animal_records[
        cow_id
    ]["activity_history"] = summary


    animal_records[
        cow_id
    ]["last_updated"] = (
        datetime.now().isoformat()
    )


    with open(
        "ai/animal_records.json",
        "w"
    ) as file:

        json.dump(
            animal_records,
            file,
            indent=4
        )


    print(
        f"Activity record updated "
        f"for Cow {cow_id}"
    )


# ======================================
# TEST
# ======================================

if __name__ == "__main__":

    print(
        "===== ACTIVITY TRACKER TEST ====="
    )


    add_activity(
        1,
        "moving"
    )

    add_activity(
        1,
        "moving"
    )

    add_activity(
        1,
        "stationary"
    )

    add_activity(
        1,
        "feeding"
    )

    add_activity(
        1,
        "drinking"
    )

    add_activity(
        1,
        "resting"
    )


    summary = get_activity_summary(1)


    print()
    print("Cow ID: 1")


    for activity, seconds in summary.items():

        print(
            f"{activity}: "
            f"{seconds} seconds"
        )