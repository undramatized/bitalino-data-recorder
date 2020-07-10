import time
import pandas as pd
import numpy as np
from bitalino import BITalino

OUTPUT_PATH = "output/data.csv"

# The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
# while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB" for devices ending with the last 4 digits of the MAC address
# ls /dev/tty.BIT* on terminal

macAddress = "/dev/tty.BITalino-A0-2D-Bluetoot"

# This will collect data for 5 sec.
running_time = 5
batteryThreshold = 30

# Channels correspond to the following
# 0 - EMG
# 1 - ECG
# 2 - EDA
# 3 - EEG
# 4 - ACC
# 5 - LUX

acqChannels = [1, 2, 4]
columns = ["seq_num", "digital_0", "digital_1",	"digital_2", "digital_3", "ecg", "eda", "acc"]
samplingRate = 1000
nSamples = 100
digitalOutput = [1, 1]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())

# Start Acquisition
device.start(samplingRate, acqChannels)

start = time.time()
end = time.time()
collected_data = []

while (end - start) < running_time:
    # Read samples
    samples = device.read(nSamples)
    print(samples, samples.shape)
    collected_data = collected_data + samples.tolist()
    end = time.time()

# Turn BITalino led on
# device.trigger(digitalOutput)

# Stop acquisition
device.stop()

# Close connection
device.close()

print(collected_data)
df = pd.DataFrame(collected_data)
df.columns = columns
print(df)
df.to_csv(OUTPUT_PATH)