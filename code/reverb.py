import numpy as np
import soundfile as sf

my_file='../files/soundtest6.wav'

data, fs = sf.read('../files/soundtest5.wav')

# Creates a 'comb' that can boost lows if the delay is tiny.
data = data * 1.2

# Reverb Setting
num_reflection=60 # 10 simulates a room
delay_gap=0.04
decay_rate=0.7

# Initialize the ouput
output_length=len(data)+int(num_reflection*delay_gap*fs)
reverb_output=np.zeros(output_length)
reverb_output[:len(data)]=data

# The reverb loop
for i in range(1, num_reflection + 1):
    jitter = np.random.uniform(-0.005, 0.005)
    # Ensure shift is never negative and stays within bounds
    shift = int(max(0, (i * delay_gap + jitter) * fs))

    attenuation = decay_rate**i
    reflection = data * attenuation

    # CUMULATIVE DAMPING
    window_size = 2 + i // 10
    reflection = np.convolve(reflection, np.ones(window_size)/window_size, mode='same')

    # --- SAFE ADDITION ---
    # We find the length of the space available in reverb_output starting from 'shift'
    available_space = len(reverb_output) - shift
    # We only take the part of the reflection that fits in that space
    actual_chunk_to_add = min(len(reflection), available_space)

    reverb_output[shift : shift + actual_chunk_to_add] += reflection[:actual_chunk_to_add]

# Normalize - Clipping
reverb_output=reverb_output/np.max(np.abs(reverb_output))

# Writing
sf.write(my_file, reverb_output, fs)
print("The Reverb file is ready!")
