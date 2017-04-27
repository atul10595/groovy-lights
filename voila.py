import pyaudio
import wave
import audioop
import os

# os.system("ls -l")
MIN = 0.01
MAX = 0.9
delta = 0
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3000 #50 minutes
# WAVE_OUTPUT_FILENAME = "output.wav"

MIN = 0
p = pyaudio.PyAudio()


def contain(delta):
    if delta > 1:
        delta = 0.96
    elif delta < 0.09:
        delta*=10

    # if delta < 0.2:
    #     delta = MIN
    if delta < 0.3:
        delta = MIN
    # elif delta < 0.7:
    #     delta = 0.7
    elif delta < 0.99:
        delta = 0.7

    return delta

def big_contain(delta):
    if(delta > 480):
        return 0.7
    else:
        return MIN


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    try:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)    # here's where you calculate the volume
        delta = rms#/float(7000)

        delta = big_contain(delta)
        os.system("brightness "+ str(delta))
    except():
        pass

    # print(delta, rms)

stream.stop_stream()
stream.close()
p.terminate()
