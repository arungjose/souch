import sounddevice as sd
import numpy as np

# Settings
FS = 44100
CHUNK_SIZE = 1024  # Tiny slices for low latency
BUFFER_SIZE = FS * 2 # 2 seconds of history
history_buffer = np.zeros(BUFFER_SIZE)

# Modulation Settings (The "Knobs")
DELAY_GAP = 0.04
DECAY_RATE = 0.6
NUM_REFLECTIONS = 5

def audio_callback(indata, outdata, frames, time, status):
    global history_buffer

    # 1. Get the mono mic data
    current_voice = indata[:, 0]

    # 2. Update History (Slide old data out, new data in)
    history_buffer = np.roll(history_buffer, -len(current_voice))
    history_buffer[-len(current_voice):] = current_voice

    # 3. Apply the Live Reverb
    # We start with the clean current voice
    mixed_output = current_voice.copy()

    for i in range(1, NUM_REFLECTIONS + 1):
        # Calculate where in the 'history' the echo is
        delay_samples = int(i * DELAY_GAP * FS)

        # Pull the 'past' sound from our buffer
        if delay_samples < BUFFER_SIZE:
            echo = history_buffer[-(delay_samples + len(current_voice)) : -delay_samples]

            # Add it to our current output
            mixed_output += echo * (DECAY_RATE ** i)

    # 4. Send to speakers (Normalizing to prevent clipping)
    outdata[:, 0] = mixed_output / (1 + DECAY_RATE)

# Start the live engine
print("Live Reverb is ACTIVE... (Use Headphones!)")
with sd.Stream(channels=1, samplerate=FS, blocksize=CHUNK_SIZE, callback=audio_callback):
    while True:
        sd.sleep(1000)
