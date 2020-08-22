import cv2
import numpy as np
import threading
from datetime import datetime


class VideoPlayer:

    OUTPUT_PATH = "../video_recordings/{filename}.mp4"
    FRAMERATE = 20.0

    def __init__(self, source):
        self.source = source
        self.playcap = cv2.VideoCapture(self.source)
        self.playing = False


        self.reccap = cv2.VideoCapture(0)
        curr_date = datetime.now().strftime("%Y_%m_%H_%M")
        self.filename = f"vidcapture_{curr_date}"
        self.out = self.create_video_writer(self.FRAMERATE)

    def rescale_frame(self, frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def is_playing(self):
        return self.playing

    def create_video_writer(self, framerate):
        width = int(self.reccap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.reccap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        return cv2.VideoWriter(self.OUTPUT_PATH.format(filename=self.filename), fourcc, framerate, (width, height))

    def create_output_frame(self, frame1, frame2):
        (h, w) = frame2.shape[:2]
        return frame2

    def play_video(self):
        # Check if camera opened successfully
        if not self.playcap.isOpened() or not self.reccap.isOpened():
            print("Error opening video file or camera")
            exit()

        # Read until video is completed
        self.playing = True
        print("playing video")
        while self.playcap.isOpened():

            # Capture frame-by-frame
            ret1, frame1 = self.playcap.read()
            ret2, frame2 = self.reccap.read()
            if ret1 and ret2:

                # Display the resulting frame
                src_frame_small = self.rescale_frame(frame1, percent=20)
                rec_frame_small = self.rescale_frame(frame2, percent=20)
                cv2.imshow('video_src', src_frame_small)
                cv2.imshow('video_rec', rec_frame_small)

                # Write frame to output file
                output = self.create_output_frame(frame1, frame2)
                self.out.write(output)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            # Break the loop
            else:
                break

        self.stop_video()

    def stop_video(self):
        print("stopping video")
        self.playing = False
        self.playcap.release()
        self.reccap.release()
        self.out.release()
        self.destroy_windows()

    def destroy_windows(self):
        # Closes all the frames
        cv2.destroyAllWindows()

    def run(self):
        player_thread = threading.Thread(target=self.play_video)
        player_thread.daemon = True
        player_thread.start()


if __name__ == '__main__':
    path = "../video_source/sample_video.mp4"
    player = VideoPlayer(path)
    player.play_video()
    # player.run()

    # while player.is_playing():
    #     print("playing video")
    #
    # print("video stopped")
