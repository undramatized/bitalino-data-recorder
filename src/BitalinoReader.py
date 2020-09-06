import time
import pandas as pd
import numpy as np
import threading
from bitalino import BITalino


class BitalinoReader:

    OUTPUT_PATH = "../output/{filename}.csv"
    MAC_ADDRESS = "/dev/tty.BITalino-A0-2D-Bluetoot"

    def __init__(self, filename, channels=[0,1,2,3,4,5], sampling_rate=1000, n_samples=100):
        self.filename = filename
        self.channels = channels
        self.sampling_rate = sampling_rate
        self.n_samples = n_samples
        self.device = self.connect()
        self.set_battery_threshold(30)
        self.recording = False
        self.data = []
        self.start_time = 0

    def connect(self):
        device = BITalino(self.MAC_ADDRESS)
        # Read BITalino version
        print("Connected to Device")
        print(device.version())
        return device

    def set_battery_threshold(self, threshold):
        self.device.battery(threshold)

    def get_columnnames(self):
        default_cols = ["timestamp", "seq_num", "digital_0", "digital_1", "digital_2", "digital_3"]
        channel_names = ["emg", "ecg", "eda", "eeg", "acc", "lux"]

        for channel in self.channels:
            default_cols.append(channel_names[channel])

        return default_cols

    def start_record(self):
        print("Starting Bitalino recording")
        self.device.start(self.sampling_rate, self.channels)
        self.recording = True
        self.start_time = time.time()
        while self.recording:
            (samples, curr_time) = self.get_data()
            time_array = np.full((self.n_samples, 1), curr_time)
            combined = np.append(time_array, samples, axis=1)
            self.data = self.data + combined.tolist()
            if not self.recording:
                break

    def get_data(self):
        samples = self.device.read(self.n_samples)
        curr_time = time.time() - self.start_time
        print(curr_time, samples)
        return (samples, curr_time)

    def stop_record(self):
        print("Stopping Bitalino record")
        self.recording = False
        self.device.stop()
        self.save_data_to_csv()
        self.close_connection()

    def save_data_to_csv(self):
        df = pd.DataFrame(self.data)
        df.columns = self.get_columnnames()
        print(df)

        filename = f"bitalino_data_{self.filename}"
        df.to_csv(self.OUTPUT_PATH.format(filename=filename))
        print("Saved data to CSV")

    def close_connection(self):
        self.device.close()
        print("Closed connection")

    def run(self):
        bitalino_thread = threading.Thread(target=self.start_record)
        bitalino_thread.start()



if __name__ == '__main__':
    bitalino = BitalinoReader(filename="rama", channels=[1,2,4])
    running_time = 5
    start = time.time()
    end = time.time()
    bitalino.run()
    while (end - start) < running_time:
        end = time.time()
        continue

    bitalino.stop_record()

