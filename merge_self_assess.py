import numpy as np
import pandas as pd
import json
import time, datetime

SELF_ACCESS_PATH = "./self_assess/"
BITALINO_DATA_PATH = "./bitalino_data/"
OUTPUT_PATH = "./formatted/"


def openSignalsFileReader(file):
    """
    Parameters
    -------
    file
        Name of the file for analysis.
    Returns
    -------
    header : JSON object
    data : array
    t : array

    """

    header = {}

    # Start acquisition of the header from file
    with open(file) as f:
        line = f.readline()
        cnt = 0
        headerlines = 3

        while line:
            if cnt <= headerlines:
                header[cnt] = line[2:]
            line = f.readline()
            cnt += 1

    # Define header
    header = json.loads(header[1])
    devices = header[list(header.keys())[0]]

    # Read "Sampling Rate" from header
    s_rate = devices['sampling rate']

    # Load data from file
    data = np.loadtxt(file)

    # Calculate the time line
    t = np.arange(len(data)) / float(s_rate)

    return (data, t, header)

def getTimelineDataframe(timeline, data, dataHeader):
    """

    :param timeline:
    :param data:
    :return: Pandas Dataframe
    """
    dataHeaderKeys = list(dataHeader.keys())
    dataCols = dataHeader[dataHeaderKeys[0]]['column']

    timelineDf = pd.DataFrame(data=timeline, columns=["time"])
    dataDf = pd.DataFrame(data=data, columns=dataCols)

    concatDf = pd.concat([timelineDf, dataDf], axis=1)

    return concatDf

def getSelfAssessDataframe(csvfilepath):
    """

    :param csvfilepath:
    :return: Pandas Dataframe
    """

    def convertTime(t):
        x = time.strptime(t, '%H:%M:%S')
        return float(datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds())

    df = pd.read_csv(csvfilepath)
    df['time'] = df['time'].apply(convertTime)

    return df

def joinSelfAssess(timelineDf, selfassessDf):

    df = timelineDf.join(selfassessDf, 'time', 'left', rsuffix='_selfassess')\
        .fillna(method='pad')\
        .drop(['time_selfassess'], axis=1)

    return df

def writeToCSV(df, filename):
    filepath = OUTPUT_PATH + filename + "_merge_formatted.csv"
    df.to_csv(filepath)


if __name__ == '__main__':
    filename = "rama_batman2_1time_2020-10-03_18-06-28.txt"
    file = BITALINO_DATA_PATH + filename

    # shows the content of the file read

    extractedData = openSignalsFileReader(file)
    timelineDf = getTimelineDataframe(extractedData[1], extractedData[0], extractedData[2])

    print(timelineDf, timelineDf.info())

    selfassessFilename = "rama_self_assess_2.csv"
    sefassessFilepath = SELF_ACCESS_PATH + selfassessFilename
    selfassessDf = getSelfAssessDataframe(sefassessFilepath)

    print(selfassessDf)

    joinDf = joinSelfAssess(timelineDf, selfassessDf)
    print(joinDf)

    writeToCSV(joinDf, "rama_batman2")