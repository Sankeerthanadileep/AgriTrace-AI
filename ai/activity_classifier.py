from enum import Enum


# ======================================
# ACTIVITY TYPES
# ======================================

class Activity(Enum):

    MOVING = "moving"

    STATIONARY = "stationary"

    FEEDING = "feeding"

    DRINKING = "drinking"

    RESTING = "resting"

    HERD_INTERACTION = "herd_interaction"

    SEPARATED = "separated"

    UNKNOWN = "unknown"


# ======================================
# MOVEMENT CLASSIFICATION
# ======================================

def classify_movement(
    movement_percentage
):

    if movement_percentage >= 20:

        return Activity.MOVING.value

    return Activity.STATIONARY.value


# ======================================
# ZONE + MOVEMENT CLASSIFICATION
# ======================================

def classify_activity(
    movement_percentage,
    zone="general_area",
    herd_size=1,
    separated=False
):

    # ----------------------------------
    # Feeding zone
    # ----------------------------------

    if zone == "feeding_area":

        return Activity.FEEDING.value


    # ----------------------------------
    # Drinking zone
    # ----------------------------------

    if zone == "drinking_area":

        return Activity.DRINKING.value


    # ----------------------------------
    # Resting zone
    # ----------------------------------

    if zone == "resting_area":

        if movement_percentage < 20:

            return Activity.RESTING.value


    # ----------------------------------
    # Separated animal
    # ----------------------------------

    if separated:

        return Activity.SEPARATED.value


    # ----------------------------------
    # Herd interaction
    # ----------------------------------

    if herd_size >= 2:

        if movement_percentage >= 20:

            return Activity.HERD_INTERACTION.value


    # ----------------------------------
    # Default movement classification
    # ----------------------------------

    return classify_movement(
        movement_percentage
    )


# ======================================
# TEST
# ======================================

if __name__ == "__main__":

    print(
        "===== ACTIVITY CLASSIFIER TEST ====="
    )

    print(
        "Moving:",
        classify_activity(
            50
        )
    )

    print(
        "Stationary:",
        classify_activity(
            5
        )
    )

    print(
        "Feeding:",
        classify_activity(
            30,
            zone="feeding_area"
        )
    )

    print(
        "Drinking:",
        classify_activity(
            10,
            zone="drinking_area"
        )
    )

    print(
        "Resting:",
        classify_activity(
            5,
            zone="resting_area"
        )
    )

    print(
        "Separated:",
        classify_activity(
            20,
            separated=True
        )
    )

    print(
        "Herd interaction:",
        classify_activity(
            30,
            herd_size=3
        )
    )