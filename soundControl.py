import os
import threading
import sounddevice as sd
import soundfile as sf
fs = 48000

class Sound (threading.Thread):
    def __init__(self, threadID):
        def callback(indata, outdata, frames, time, status):
            if status:
                print(status)
            outdata[:] = indata
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.stream = sd.Stream(channels=2, callback=callback)

    def startCallback(self,song,playVolume,vocalVolume):
        fname = f"./songs/{song}/audio/accompaniment.wav"
        vocal = f"./songs/{song}/audio/vocals.wav"
        accompaniment, fs = sf.read(fname, dtype="float32")
        vocal, fs = sf.read(vocal, dtype="float32")
        sd.play(vocal*playVolume*vocalVolume + accompaniment*playVolume,fs)
        self.stream.start()

    def stopCallback(self):
        self.stream.stop()
        sd.stop()
