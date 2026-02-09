import sounddevice as sd
import soundfile as sf

fs=44100
seconds=5
rec_file='../files/soundtest5.wav'

print(f"Recording started for {seconds} seconds!!")
my_recording=sd.rec(int(seconds*fs), samplerate=fs, channels=1)

sd.wait()

print("Recording has ended!!")
sf.write(rec_file, my_recording, fs)

print("Recording is saved!")
