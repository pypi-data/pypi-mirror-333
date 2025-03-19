import os
import struct
from typing import Any

from intan.channels import Channel


# Version 3.0, 11 February 2021

# Reads spike.dat files generated by Intan Technologies RHX data acqusition
# software.  Data are parsed and placed into variables within the Python workspace.
# Therefore, it is recommended to add either saving these variables to disk or
# any plotting or processing of the data at the end of readIntanSpikeFile, before
# those variables are removed when execution completes

# Spike data from N channels are loaded into an N x M list named
# 'spikes', where M = 5 if spike snapshots were saved, otherwise M = 4.
# The first column of spikes contains native channel names.  The second
# column contains custom channel names.  The third column contains spike
# timestamps.  The fourth column contains spike ID numbers (128 = likely
# artifact due to amplitude exceeding threshold set in Spike Scope).  All 
# normal spikes have a spike ID of 1.  Future versions of the RHX software
# may support realtime spike sorting, and in this case spike ID will 
# denote different identified spikes (1, 2, 3, etc.).  If spike snapshots
# were saved then they are contained in the fifth column.

def read_intan_spike_file(full_file_name, no_artifacts=True) -> tuple[list[list[Any]], float]:
    """
    # Spike data from N channels are loaded into an N x M list named
    # 'spikes', where M = 5 if spike snapshots were saved, otherwise M = 4.
    # The first column of spikes contains native channel names.  The second
    # column contains custom channel names.  The third column contains spike
    # timestamps.  The fourth column contains spike ID numbers (128 = likely
    # artifact due to amplitude exceeding threshold set in Spike Scope).  All
    # normal spikes have a spike ID of 1.  Future versions of the RHX software
    # may support realtime spike sorting, and in this case spike ID will
    # denote different identified spikes (1, 2, 3, etc.).  If spike snapshots
    # were saved then they are contained in the fifth column.
    """

    # Open data file
    fid = open(full_file_name, 'rb')
    filesize = os.path.getsize(full_file_name)

    # Check 'magic number' at beginning of file to make sure this is an Intan
    # Technologies spike data file.
    magicNumber, = struct.unpack('<I', fid.read(4))
    if magicNumber == int('18f8474b', 16):
        multichannel = 1
    elif magicNumber == int('18f88c00', 16):
        multichannel = 0
    else:
        raise Exception('Unrecognized file type.')

    spikeFileVersionNumber, = struct.unpack('<H', fid.read(2))

    if spikeFileVersionNumber > 1:
        print("Warning: This spike file version is not supported by this file reader.")
        print("Check the Intan Technologies website for a more recent version.")

    filename = readString(fid)
    channelList = readString(fid).split(",")
    customChannelList = readString(fid).split(",")

    sample_rate, = struct.unpack('<f', fid.read(4))

    samplesPreDetect, = struct.unpack('<I', fid.read(4))
    samplesPostDetect, = struct.unpack('<I', fid.read(4))
    nSamples = samplesPreDetect + samplesPostDetect

    if nSamples == 0:
        snapshotsPresent = 0
    else:
        snapshotsPresent = 1

    N = len(channelList)

    spikes = [[] for _ in range(N)]
    for i in range(N):
        spikes[i].append(channelList[i])  # 0: native channel name
        spikes[i].append(customChannelList[i])  # 1: custom channel name
        spikes[i].append([])  # 2: single-float timestamp
        spikes[i].append([])  # 3: uint8 spike ID
        if snapshotsPresent:
            spikes[i].append([])  # 4: single-float snapshot

    while filesize - fid.tell() > 0:
        if multichannel:
            channelName = ""
            for charIndex in range(5):
                thisChar, = struct.unpack('<c', fid.read(1))
                channelName = channelName + str(thisChar, "utf-8")
            for i in range(N):
                if spikes[i][0] == channelName:
                    index = i
                    break
        else:
            index = 1

        timestamp, = struct.unpack('<i', fid.read(4))
        spikeID, = struct.unpack('<B', fid.read(1))

        if snapshotsPresent:
            snapshot = list(struct.unpack("<%dH" % nSamples, fid.read(2 * nSamples)))

        if spikeID == 128 and no_artifacts:
            continue

        timestampSeconds = timestamp / sample_rate

        spikes[index][2].append(timestampSeconds)
        spikes[index][3].append(spikeID)
        if snapshotsPresent:
            snapshotMicroVolts = [0.195 * (float(snapshotSample) - 32768.0) for snapshotSample in snapshot]
            spikes[i][4].append(snapshotMicroVolts)

    # Close data file
    fid.close()

    return spikes, sample_rate

    #
    # if snapshotsPresent:
    #     tSnapshot = [(sample - samplesPreDetect) / sampleRate for sample in range(nSamples)]
    #
    # # Just for demonstration, take the plot the 2nd (N = 1) channel's list of snapshots (snapshots are always
    # # in the fifth column M = 4). Grab the 6th snapshot present (list index = 5) and plot it
    # secondChannelSnapshots = spikes[1][4]
    # plt.plot(tSnapshot, secondChannelSnapshots[5])
    # plt.show()


def readString(fid):
    resultStr = ""
    ch, = struct.unpack('<c', fid.read(1))
    while ch != b'\0':
        resultStr = resultStr + str(ch, "utf-8")
        ch, = struct.unpack('<c', fid.read(1))
    return resultStr


# If the function is called with the "noartifacts" parameter, all spikes with spike ID = 128 are ignored.
# readIntanSpikeFile("artifacts")
# #readIntanSpikeFile("noartifacts")
def spike_matrix_to_spike_tstamps_for_channels(spike_matrix) -> dict[Channel: list[float]]:
    """
    Convert spike data into a dictionary of channel names and responses.
    """
    spike_dict = {}
    for row in spike_matrix:
        channel_name = str_to_channel_enum(row[0])
        responses = row[2]
        spike_dict[channel_name] = responses
    return spike_dict


def str_to_channel_enum(str_value):
    enum_name = str_value.replace('-', '_')
    try:
        return getattr(Channel, enum_name)
    except AttributeError:
        raise ValueError(f"{str_value} is not a valid member of {Channel.__name__}")


def fetch_spike_tstamps_from_file(spike_file_path: str) -> tuple[Any, float]:
    spike_matrix, sample_rate = read_intan_spike_file(spike_file_path)
    spike_tstamps_for_channels = spike_matrix_to_spike_tstamps_for_channels(spike_matrix)
    return spike_tstamps_for_channels, sample_rate
