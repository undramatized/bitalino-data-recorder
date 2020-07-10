import cv2
import numpy as np

VIDEO_PATH = "video_source/sample_video.mp4"


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(VIDEO_PATH)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Read until video is completed
while cap.isOpened():

    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:

        # Display the resulting frame
        frame_small = rescale_frame(frame, percent=20)
        cv2.imshow('video_src', frame_small)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()