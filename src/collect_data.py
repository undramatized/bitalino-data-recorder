from src.BitalinoReader import BitalinoReader
from src.VideoPlayer import VideoPlayer
from datetime import datetime

if __name__ == '__main__':
    subject_name = "rama"
    curr_datetime = datetime.now().strftime("%Y_%m_%H_%M")
    filename = subject_name + '_' + curr_datetime

    video_path = "../video_source/sample_video.mp4"

    bitalino_thread = BitalinoReader(filename, channels=[1,2,4])
    video_thread = VideoPlayer(video_path, filename)

    bitalino_thread.run()
    video_thread.start()

    while video_thread.is_playing():
        continue

    bitalino_thread.stop_record()


