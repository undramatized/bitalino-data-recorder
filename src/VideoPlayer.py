import cv2
import numpy as np
import threading
from datetime import datetime
import time
from collections import deque


class VideoPlayer:

    OUTPUT_PATH = "../video_recordings/{filename}.mp4"
    FRAMERATE = 23.98

    def __init__(self, source, filename):
        self.source = source
        self.filename = filename
        self.vidret = self.vidframe = self.status = self.frame = None
        self.vidframes = deque()

        self.playcap = cv2.VideoCapture(self.source)
        self.playing = False
        self.writing = False

        self.reccap = cv2.VideoCapture(0)

        self.out = self.create_video_writer(self.FRAMERATE)

    def rescale_frame(self, frame, percent=75):
        '''
        Method to resize CV2 frame
        :param frame: cv2 frame - input
        :param percent: int - percentage to resize by
        :return: cv2 frame - resized
        '''
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def is_playing(self):
        '''
        Method to get self.playing
        :return: boolean
        '''
        return self.playing

    def update_cam(self):
        '''
        Method to read frames from the webcam and update the self.frame and self.status
        Executed in a seperate thread by read_thread
        :return: None
        '''
        # Read the next frame from the stream in a different thread
        while True:
            if self.reccap.isOpened():
                (self.status, self.frame) = self.reccap.read()
            time.sleep(.01)

    def write_output(self):
        '''
        Method to write the composite frames into the output file
        Executed in a seperate thread by write_thread
        :return: None
        '''
        # Read the next frame from the stream in a different thread
        while True:
            try:
                if self.is_playing():
                    frame = self.vidframes.popleft()
                    src_frame_small = self.rescale_frame(frame, percent=10)
                    output = self.create_output_frame(src_frame_small, self.frame)
                    self.out.write(output)
                    # self.out.write(self.frame)
            except:
                continue
            time.sleep(.01)

    def create_video_writer(self, framerate):
        '''
        Creates VideoWriter class, defining codec, framerate, width/height and output filename
        :param framerate:
        :return: VideoWriter class object
        '''
        width = int(self.reccap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.reccap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        filename = f"{self.filename}"
        return cv2.VideoWriter(self.OUTPUT_PATH.format(filename=filename), fourcc, framerate, (width, height))

    def create_output_frame(self, frame1, frame2):
        '''
        Takes in two frames, and creates a composite of one frame as small overlay over other.
        :param frame1: vid_src
        :param frame2: webcam_recording
        :return: CV2 composite frame
        '''
        (h, w) = frame1.shape[:2]
        x_offset = y_offset = 50
        frame2[y_offset:y_offset + h, x_offset:x_offset + w] = frame1
        return frame2

    def start(self):
        '''
        Main function to run.

        Checks if camera and video sources are working.
        Starts playing video and adds frames to the self.vidframes deque.
        When video ends OR 'q' key is pressed, process will stop.
        :return:
        '''
        # Check if camera opened successfully
        if not self.playcap.isOpened() or not self.reccap.isOpened():
            print("Error opening video file or camera")
            exit()

        # Start the read thread for webcam
        print("playing video")
        self.read_thread()
        self.playing = True

        # continue while video is playing
        while self.playcap.isOpened():

            # Play video frame-by-frame
            self.vidret, self.vidframe = self.playcap.read()
            if self.vidret:
                self.vidframes.append(self.vidframe)
                if not self.writing:
                    self.write_thread()
                    self.writing = True

                # Display the resulting frame
                src_frame_medium = self.rescale_frame(self.vidframe, percent=20)
                cv2.imshow('video_src', src_frame_medium)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            # Break the loop
            else:
                break

        self.stop()

    def stop(self):
        '''
        Stops input from both sources.
        Stops VideoWriter.
        Destroys all windows.
        :return:
        '''
        print("stopping video")
        self.playing = False
        self.playcap.release()
        self.reccap.release()
        self.out.release()
        self.destroy_windows()

    def destroy_windows(self):
        '''
        Closes all frames and windows (GUI)
        :return:
        '''
        cv2.destroyAllWindows()

    def read_thread(self):
        '''
        Thread for reading from the webcam input
        :return:
        '''
        reader_thread = threading.Thread(target=self.update_cam)
        reader_thread.daemon = True
        reader_thread.start()

    def write_thread(self):
        '''
        Thread for writing into the output file
        :return:
        '''
        writer_thread = threading.Thread(target=self.write_output)
        writer_thread.daemon = True
        writer_thread.start()


if __name__ == '__main__':
    subject_name = "rama"
    curr_datetime = datetime.now().strftime("%Y_%m_%H_%M")
    filename = subject_name + '_' + curr_datetime
    path = "../video_source/batman_returns_2.mp4"
    player = VideoPlayer(path, filename)
    player.start()

