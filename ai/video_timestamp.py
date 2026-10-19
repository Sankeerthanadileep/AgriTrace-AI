def frame_to_timestamp(frame_number, fps):
    """
    Convert a video frame number into HH:MM:SS format.
    """

    total_seconds = int(frame_number / fps)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def frame_to_seconds(frame_number, fps):
    """
    Convert a frame number into seconds.
    """

    return round(frame_number / fps, 2)


if __name__ == "__main__":

    FPS = 25.0

    print("===== VIDEO TIMESTAMP TEST =====")

    print(
        "Frame 0:",
        frame_to_timestamp(0, FPS)
    )

    print(
        "Frame 625:",
        frame_to_timestamp(625, FPS)
    )

    print(
        "Frame 1250:",
        frame_to_timestamp(1250, FPS)
    )

    print(
        "Frame 625 in seconds:",
        frame_to_seconds(625, FPS)
    )