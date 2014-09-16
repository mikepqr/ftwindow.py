import sys
import numpy as np


def hex2binLines(hexString):
    '''
    convert hexadecimal string of length N to list of N/2 8-character binary
    strings, where N is an even integer
    '''

    # split into list of 2-character hex strings
    hexStrings = [hexString[i:i+2] for i in range(0, len(hexString), 2)]

    # convert to padded binary representation
    binLines = map(lambda s: "{0:08b}".format(int(s, 16)), hexStrings)

    return binLines


def parseFrames():
    '''
    parse frames.txt entries into list of dicts. frames.txt is available with
    curl -O http://labs.brandwatch.com/FTWindow/twitterdata/frames.txt
    '''
    filename = 'frames.txt'
    tweets = []
    with open(filename) as f:
        for line in f:
            words = line.split()
            tweets.append({
                'time': words[0],
                'user': words[1],
                'screen': words[2],
                'data': words[3:]
            })
    return tweets


def extractAllData(tweets):
    '''
    Given dict of frames.txt, return list of hex strings
    '''
    data = []
    for tweet in tweets:
        data += tweet['data']
    return data


def renderBinLine(binLine):
    '''
    Returns a string of 'X' and ' ' given a string of '1' and '0'
    '''
    return ''.join(map(lambda s: ' ' if s == '0' else 'X', binLine))


def renderData(data):
    '''
    Returns ascii representation of a hex string or list of binary strings
    '''
    binLines = hex2binLines(data)
    asciiLines = map(renderBinLine, binLines)
    return '\n'.join(asciiLines)


def data2array(data):
    '''
    Convert hex string or list of binary strings to a numpy array
    '''
    binLines = hex2binLines(data)
    return np.array([[int(i) for i in binLine] for binLine in binLines])


def array2data(X):
    '''
    Returns N digit hex representation of an (N/2, 8) numpy array of 1s and 0s
    '''
    # Convert each line to 8-digit binary string
    binLines = [''.join([str(i) for i in j]) for j in X]
    hexString = ''.join(['{0:02X}'.format(int(i, 2)) for i in binLines])
    return hexString


def averageData(threshold=False):
    '''
    Returns the average image in numpy array form
    '''
    tweets = parseFrames()  # dictionary
    allData_strings = extractAllData(tweets)  # list of hex strings
    allData_arrays = map(data2array, allData_strings)  # list of np arrays
    sumData = reduce(lambda x, y: x + y, allData_arrays)
    avgData = sumData.astype(float)/len(tweets)

    # Plot with e.g.
    # >>> plt.axis('off')
    # >>> plt.imshow(avgData_array, interpolation="nearest");
    # or threshold the data
    avgData_threshold = np.zeros_like(sumData)
    avgData_threshold[avgData > np.median(avgData)] = 1
    print array2data(avgData_threshold)

    if threshold:
        return avgData_threshold
    else:
        return avgData
