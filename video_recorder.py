import numpy as np
import cv2
from datetime import datetime

OUTPUT_PATH = "video_recordings/{filename}.mp4"

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

cap = cv2.VideoCapture(0)
curr_date = datetime.now().strftime("%Y_%m_%H_%M")
filename = f"vidcapture_{curr_date}"

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
framerate = 20.0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH.format(filename=filename), fourcc, framerate, (640,  480))

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    frame_small = rescale_frame(frame, percent=20)
    # Write frame to output file
    out.write(frame)
    # Display the resulting frame
    cv2.imshow('frame', frame_small)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()