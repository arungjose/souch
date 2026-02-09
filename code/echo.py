import numpy as np
import soundfile as sf

my_file='../files/soundtest3.wav'

data, fs = sf.read('../files/soundtest2.wav')

delay_seconds=0.3
delay_samples=int(delay_seconds*fs)
reduction_factor=0.5

# The Ghost signal
echo_signal=np.zeros(len(data)+delay_samples)

# Places original sound into echo, but it is shifted forward
echo_signal[delay_samples:] = data * reduction_factor

# Original audio to match the echo
original_extended=np.zeros(len(data)+delay_samples)
original_extended[:len(data)] = data

# Mixing the original and echo together
combined_signal = original_extended + echo_signal

# Normalize (Safety Step)
# Adding waves can make them "too loud" (clipping). We shrink it back to fit -1.0 to 1.0.
combined_signal=combined_signal/np.max(np.abs(combined_signal))

# Writing
sf.write(my_file, combined_signal, fs)
print("The echo sound is ready!!")
