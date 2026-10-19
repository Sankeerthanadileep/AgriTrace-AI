import json
from collections import defaultdict

import cv2
from ultralytics import YOLO

from activity_classifier import classify_activity
from activity_tracker import add_activity, get_activity_summary
from appearance_identity import AppearanceIdentityManager
from farm_zones import get_zone


# ======================================
# AGRITRACE AI SETTINGS
# ======================================

VIDEO_PATH = "videos/farm_video.mp4"
OUTPUT_VIDEO_PATH = "videos/agritrace_annotated.mp4"

COW_CLASS_ID = 19

FPS = 30.0

MOVEMENT_THRESHOLD = 5

IDENTITY_DISTANCE_THRESHOLD = 120


# ======================================
# START
# ======================================

print("======================================")
print("      AgriTrace AI - AI Pipeline")
print("======================================")

print("Loading YOLO model...")

model = YOLO("yolo11n.pt")

identity_manager = AppearanceIdentityManager(
    max_distance=IDENTITY_DISTANCE_THRESHOLD
)

print("Model loaded.")


# ======================================
# OPEN VIDEO
# ======================================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Could not open video.")
    exit()


video_fps = cap.get(cv2.CAP_PROP_FPS)

if video_fps <= 0:
    video_fps = FPS


frame_width = int(
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)

frame_height = int(
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)

total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)


print()
print("Video information:")
print(
    f"Resolution: {frame_width} x {frame_height}"
)
print(f"FPS: {video_fps}")
print(f"Total frames: {total_frames}")


# ======================================
# CREATE OUTPUT VIDEO
# ======================================

fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)

writer = cv2.VideoWriter(
    OUTPUT_VIDEO_PATH,
    fourcc,
    video_fps,
    (frame_width, frame_height)
)


# ======================================
# ANIMAL STATE
# ======================================

cow_state = defaultdict(
    lambda: {
        "previous_center": None,
        "tracking_id": None,
        "frames_seen": 0,
        "last_zone": "general_area"
    }
)


# ======================================
# PROCESS VIDEO
# ======================================

print()
print("Processing video...")
print()


frame_count = 0


while True:

    success, frame = cap.read()

    if not success:
        break

    frame_count += 1


    # ----------------------------------
    # YOLO TRACKING
    # ----------------------------------

    results = model.track(
        frame,
        tracker="bytetrack.yaml",
        persist=True,
        classes=[COW_CLASS_ID],
        verbose=False
    )

    result = results[0]


    # ----------------------------------
    # DETECTED ANIMALS
    # ----------------------------------

    if result.boxes.id is not None:

        track_ids = (
            result.boxes.id
            .int()
            .cpu()
            .tolist()
        )

        boxes = (
            result.boxes.xyxy
            .cpu()
            .tolist()
        )

        herd_size = len(track_ids)


        # ----------------------------------
        # PROCESS EACH ANIMAL
        # ----------------------------------

        for tracking_id, box in zip(
            track_ids,
            boxes
        ):

            tracking_id = str(
                tracking_id
            )


            # Bounding box

            x1, y1, x2, y2 = map(
                int,
                box
            )


            # Animal center

            center_x = (
                x1 + x2
            ) / 2

            center_y = (
                y1 + y2
            ) / 2

            center = (
                center_x,
                center_y
            )


            # ----------------------------------
            # ANIMAL IDENTITY
            # ----------------------------------

            animal_id = (
                identity_manager
                .get_or_create(
                    tracking_id,
                    center
                )
            )


            cow_state[
                animal_id
            ]["tracking_id"] = tracking_id


            cow_state[
                animal_id
            ]["frames_seen"] += 1


            # ----------------------------------
            # MOVEMENT
            # ----------------------------------

            previous = cow_state[
                animal_id
            ]["previous_center"]


            if previous is None:

                movement = 0

            else:

                previous_x, previous_y = (
                    previous
                )

                movement = (
                    (center_x - previous_x) ** 2
                    +
                    (center_y - previous_y) ** 2
                ) ** 0.5


            if movement > MOVEMENT_THRESHOLD:

                movement_percentage = 100

            else:

                movement_percentage = 0


            # ----------------------------------
            # FARM ZONE
            # ----------------------------------

            zone = get_zone(
                center_x,
                center_y
            )


            cow_state[
                animal_id
            ]["last_zone"] = zone


            # ----------------------------------
            # ACTIVITY
            # ----------------------------------

            activity = classify_activity(
                movement_percentage=
                    movement_percentage,

                zone=zone,

                herd_size=herd_size,

                separated=False
            )


            add_activity(
                animal_id,
                activity
            )


            # Save current position

            cow_state[
                animal_id
            ]["previous_center"] = center


            # ==================================
            # DRAW ANIMAL BOX
            # ==================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # ==================================
            # ANIMAL LABEL
            # ==================================

            activity_text = (
                activity
                .replace("_", " ")
                .title()
            )


            label = (
                f"{animal_id} | "
                f"{activity_text}"
            )


            # ==================================
            # LABEL SIZE
            # ==================================

            font = (
                cv2.FONT_HERSHEY_SIMPLEX
            )

            font_scale = 0.55

            thickness = 2


            text_size = (
                cv2.getTextSize(
                    label,
                    font,
                    font_scale,
                    thickness
                )[0]
            )


            text_width = text_size[0]

            text_height = text_size[1]


            # ==================================
            # LABEL POSITION
            # ==================================

            label_x = x1

            label_y = max(
                y1 - 10,
                text_height + 10
            )


            # ==================================
            # LABEL BACKGROUND
            # ==================================

            cv2.rectangle(
                frame,

                (
                    label_x,
                    label_y - text_height - 8
                ),

                (
                    label_x + text_width + 10,
                    label_y + 5
                ),

                (0, 0, 0),

                -1
            )


            # ==================================
            # LABEL TEXT
            # ==================================

            cv2.putText(
                frame,

                label,

                (
                    label_x + 5,
                    label_y
                ),

                font,

                font_scale,

                (255, 255, 255),

                thickness,

                cv2.LINE_AA
            )


    # ======================================
    # VIDEO INFORMATION
    # ======================================

    info_text = (
        f"AgriTrace AI | "
        f"Frame {frame_count}/{total_frames}"
    )


    cv2.putText(
        frame,

        info_text,

        (20, 35),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.7,

        (255, 255, 255),

        2,

        cv2.LINE_AA
    )


    # ======================================
    # SAVE FRAME
    # ======================================

    writer.write(frame)


    # Progress

    if frame_count % 100 == 0:

        print(
            f"Processed "
            f"{frame_count}/"
            f"{total_frames} frames"
        )


# ======================================
# CLOSE VIDEO
# ======================================

cap.release()

writer.release()


print()
print("Video processing completed.")

print(
    "Annotated video saved to:"
)

print(
    OUTPUT_VIDEO_PATH
)


# ======================================
# CREATE ANIMAL RECORDS
# ======================================

animal_records = {}


for animal_id in cow_state:

    summary = get_activity_summary(
        animal_id
    )


    moving = (
        summary["moving_seconds"]
    )

    stationary = (
        summary["stationary_seconds"]
    )

    feeding = (
        summary["feeding_seconds"]
    )

    drinking = (
        summary["drinking_seconds"]
    )

    resting = (
        summary["resting_seconds"]
    )


    total_activity = (
        moving
        + stationary
        + feeding
        + drinking
        + resting
    )


    if total_activity == 0:

        continue


    # ----------------------------------
    # CURRENT ACTIVITY
    # ----------------------------------

    activity_times = {

        "moving": moving,

        "stationary": stationary,

        "feeding": feeding,

        "drinking": drinking,

        "resting": resting
    }


    current_activity = max(
        activity_times,
        key=activity_times.get
    )


    moving_percentage = (
        moving /
        total_activity
    ) * 100


    stationary_percentage = (
        stationary /
        total_activity
    ) * 100


    tracking_id = cow_state[
        animal_id
    ]["tracking_id"]


    frames_seen = cow_state[
        animal_id
    ]["frames_seen"]


    observed_seconds = (
        frames_seen /
        video_fps
    )


    # ----------------------------------
    # ANIMAL RECORD
    # ----------------------------------

    animal_records[
        animal_id
    ] = {

        "animal_id": animal_id,


        "identity": {

            "tracking_id":
                tracking_id,

            "identity_method":
                "video_position_reidentification",

            "permanent_id":
                None
        },


        "behavior_baseline": {

            "observed_seconds":
                0,

            "moving_percentage":
                0,

            "stationary_percentage":
                0
        },


        "current_behavior": {

            "activity":
                current_activity,

            "moving_percentage":
                round(
                    moving_percentage,
                    2
                ),

            "stationary_percentage":
                round(
                    stationary_percentage,
                    2
                )
        },


        "activity_history":
            summary,


        "observation": {

            "frames_seen":
                frames_seen,

            "observed_seconds":
                round(
                    observed_seconds,
                    2
                ),

            "last_zone":
                cow_state[
                    animal_id
                ]["last_zone"]
        },


        "events": [],


        "alerts": [],


        "farm_records": {

            "breed":
                None,

            "age":
                None,

            "weight":
                None,

            "vaccinations":
                [],

            "breeding_records":
                [],

            "milk_production":
                [],

            "veterinary_records":
                []
        }
    }


# ======================================
# SAVE RECORDS
# ======================================

with open(
    "ai/animal_records.json",
    "w"
) as file:

    json.dump(
        animal_records,
        file,
        indent=4
    )


# ======================================
# DISPLAY RESULTS
# ======================================

print()
print(
    "===== AGRITRACE ANIMAL ACTIVITIES ====="
)


for animal_id, data in (
    animal_records.items()
):

    activity = data[
        "current_behavior"
    ]["activity"]


    zone = data[
        "observation"
    ]["last_zone"]


    print(
        f"{animal_id} | "
        f"Activity: {activity} | "
        f"Zone: {zone}"
    )


print()
print(
    "======================================"
)

print(
    "          AI PIPELINE COMPLETE"
)

print(
    "======================================"
)

print()
print(
    "Annotated video:"
)

print(
    OUTPUT_VIDEO_PATH
)