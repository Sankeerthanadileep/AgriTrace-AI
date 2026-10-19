import cv2

VIDEO_PATH = "videos/farm_video.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

duration = frame_count / fps

print(f"FPS: {fps}")
print(f"Total frames: {int(frame_count)}")
print(f"Duration: {duration:.2f} seconds")

cap.release()