import pyaudio
import numpy as np
import time
class Sender:    
    def __init__(self, volume = 1, fs = 44100, duration = 0.5):
        self.volume = volume
        self.fs = fs
        self.duration = duration
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, 
            rate=self.fs, output=True) 
        self.array = np.arange(self.fs*duration)

    def send(self, freq):
        pulse = np.sin(2*np.pi*self.array*freq/self.fs).astype(np.float32)
        self.stream.write(self.volume*pulse)
        self.stream.write(0*pulse)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
