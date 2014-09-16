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
    binLines = map(
        lambda s: "{0:08b}".format(int(s, 16)), hexStrings)

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


def checkBinLines(s):
    '''
    Convert to list of binary strings if not already in that form
    '''
    if type(s) is str:  # FIXME: this is not a foolproof test
        return hex2binLines(s)
    else:
        return binLines


def renderBinLine(binLine):
    '''
    Returns a string of 'X' and ' ' given a string of '1' and '0'
    '''
    return ''.join(map(lambda s: ' ' if s == '0' else 'X', binLine))


def renderData(data):
    '''
    Returns ascii representation of a hex string or list of binary strings
    '''
    binLines = checkBinLines(data)
    asciiLines = map(renderBinLine, binLines)
    return '\n'.join(asciiLines)


def data2array(data):
    '''
    Convert hex string or list of binary strings to a numpy array
    '''
    X = np.zeros((16, 8))
    binLines = checkBinLines(data)
    for i in range(16):
        X[i] = [str(j) for j in binLines[i]]
    return X


def array2data(X):
    '''
    Returns 32 digit hex representation of a (16,8) numpy array of 1s and 0s
    '''
    hexString = ''
    # For each row of array...
    for i in range(16):
        # Convert to 8-digit binary string
        binLine = reduce(lambda x, y: str(int(x)) + str(int(y)), X[i, :])
        # Convert to 2-digit hex string and append
        hexString += '{0:02X}'.format(int(binLine, 2))
    return hexString


def averageData(threshold=False):
    '''
    Returns the average image in numpy array form
    '''
    tweets = parseFrames()  # dictionary
    allData_strings = extractAllData(tweets)  # list of hex strings
    allData_arrays = map(data2array, allData_strings)  # list of np arrays
    avgData = reduce(lambda x, y: x + y, allData_arrays)/len(tweets)

    # Plot with e.g.
    # >>> plt.axis('off')
    # >>> plt.imshow(avgData_array, interpolation="nearest");
    # or threshold the data
    avgData_threshold = np.zeros_like(avgData)
    avgData_threshold[avgData > np.median(avgData)] = 1
    print array2data(avgData_threshold)

    if threshold:
        return avgData_threshold
    else:
        return avgData
