import cv2
import os

VIDEO_PATH = "videos/farm_video.mp4"
OUTPUT_PATH = "ai/farm_frame.jpg"

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Could not open video.")
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("Total frames:", total_frames)

# Select middle frame
frame_number = total_frames // 2

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

success, frame = cap.read()

if not success or frame is None:
    print("ERROR: Could not read frame.")
    cap.release()
    exit()

print("Frame shape:", frame.shape)

success = cv2.imwrite(OUTPUT_PATH, frame)

if success:
    file_size = os.path.getsize(OUTPUT_PATH)

    print("Frame saved successfully.")
    print("Path:", OUTPUT_PATH)
    print("File size:", file_size, "bytes")
else:
    print("ERROR: Could not save image.")

cap.release()