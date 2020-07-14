import cv2
import numpy as np
import threading


class VideoPlayer:

    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(self.source)
        self.playing = False

    def rescale_frame(self, frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def is_playing(self):
        return self.playing

    def play_video(self):
        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("Error opening video file")

        # Read until video is completed
        self.playing = True
        print("playing video")
        while self.cap.isOpened():

            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret:

                # Display the resulting frame
                frame_small = self.rescale_frame(frame, percent=20)
                cv2.imshow('video_src', frame_small)

                # # Press Q on keyboard to  exit
                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     break

            # Break the loop
            else:
                break

        self.stop_video()

    def stop_video(self):
        print("stopping video")
        self.playing = False
        self.cap.release()
        self.destroy_windows()

    def destroy_windows(self):
        # Closes all the frames
        cv2.destroyAllWindows()

    def run(self):
        player_thread = threading.Thread(target=self.play_video)
        player_thread.start()


if __name__ == '__main__':
    path = "../video_source/sample_video.mp4"
    player = VideoPlayer(path)
    player.play_video()

    # while player.is_playing():
    #     print("playing video")
    #
    # print("video stopped")
