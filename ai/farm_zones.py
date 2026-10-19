# ======================================
# AGRITRACE AI - FARM ZONES
# ======================================

# Video resolution:
# 1024 x 576
#
# Layout:
# LEFT   -> Feeding
# CENTER -> General / cow movement
# RIGHT  -> Drinking
# TOP    -> Resting
# BOTTOM -> General


FARM_ZONES = {

    # ------------------------------
    # RESTING AREA
    # ------------------------------
    "resting_area": {
        "x1": 0,
        "y1": 0,
        "x2": 1024,
        "y2": 150
    },

    # ------------------------------
    # FEEDING AREA
    # ------------------------------
    "feeding_area": {
        "x1": 0,
        "y1": 150,
        "x2": 300,
        "y2": 576
    },

    # ------------------------------
    # DRINKING AREA
    # ------------------------------
    "drinking_area": {
        "x1": 724,
        "y1": 150,
        "x2": 1024,
        "y2": 576
    }
}


# ======================================
# FIND ANIMAL ZONE
# ======================================

def get_zone(center_x, center_y):

    for zone_name, zone in FARM_ZONES.items():

        if (
            zone["x1"] <= center_x <= zone["x2"]
            and
            zone["y1"] <= center_y <= zone["y2"]
        ):
            return zone_name

    return "general_area"


# ======================================
# TEST
# ======================================

if __name__ == "__main__":

    print("===== FARM ZONE TEST =====")

    test_points = [
        ("Top", 500, 80),
        ("Left", 150, 300),
        ("Right", 850, 300),
        ("Center", 500, 300),
        ("Bottom", 500, 520)
    ]

    for name, x, y in test_points:

        zone = get_zone(x, y)

        print(
            f"{name}: "
            f"({x}, {y}) -> {zone}"
        )