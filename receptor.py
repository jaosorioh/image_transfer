import pyaudio
import numpy as np

class Listener:
    def __init__(self, fs = 44100, duration = 4/20):
        self.fs = fs
        self.duration = duration
        self.CHUNK = int(self.duration*self.fs)
        self.p=pyaudio.PyAudio() # start the PyAudio class
        self.stream=self.p.open(format=pyaudio.paInt32,channels=1,rate=self.fs,input=True,
              frames_per_buffer=self.CHUNK) #uses default input device

    def listen(self):
        data = np.fromstring(self.stream.read(self.CHUNK),dtype=np.int32)
        data = data * np.hanning(len(data)) # smooth the FFT by windowing data
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        freq = np.fft.fftfreq(self.CHUNK,1.0/self.fs)
        freq = freq[:int(len(freq)/2)] # keep only first half    
        freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1        
        return freqPeak

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()