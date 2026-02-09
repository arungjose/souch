import sounddevice as sd
import numpy as np

# --- CONFIGURATION ---
FS = 44100          # Sample Rate
CHUNK_SIZE = 1024   # Small chunk = Low Latency
BUFFER_SIZE = 44100 # 1 second of audio memory

# Reverb "Knobs"
ROOM_SIZE = 0.8    # 30ms delay gap (Smaller = more metallic, Larger = more cave-like)
DAMPING = 0.4       # How much high-end is lost per bounce
FEEDBACK = 0.8      # How long the reverb lasts (0.1 to 0.9)

# Global memory to store the "History" of your voice
history_buffer = np.zeros(BUFFER_SIZE, dtype=np.float32)

def audio_callback(indata, outdata, frames, time, status):
    global history_buffer

    if status:
        print(status)

    # 1. Grab current microphone input
    current_chunk = indata[:, 0]

    # 2. Update the History Buffer (Slide old sound out, new sound in)
    history_buffer = np.roll(history_buffer, -len(current_chunk))
    history_buffer[-len(current_chunk):] = current_chunk

    # 3. Create the Reverb "Reflection"
    # We look back into the history by 'ROOM_SIZE' seconds
    delay_samples = int(ROOM_SIZE * FS)

    # Pull the past sound
    # We grab a slice from the past that matches the current chunk size
    start_idx = BUFFER_SIZE - delay_samples - len(current_chunk)
    end_idx = BUFFER_SIZE - delay_samples
    past_sound = history_buffer[start_idx:end_idx]

    # 4. Apply Damping (The "Bass" secret)
    # We smooth the past sound to make it sound muffled/bassy
    past_sound = (past_sound + np.roll(past_sound, 1)) / 2

    # 5. MIXING
    # Current Voice + (Past Sound * Feedback)
    output = current_chunk + (past_sound * FEEDBACK)

    # 6. Normalize to prevent ear-piercing "clipping"
    outdata[:, 0] = output / 1.7

# --- START THE ENGINE ---
print(f"Engine LIVE. Room Size: {ROOM_SIZE}s | Feedback: {FEEDBACK}")
print("USE HEADPHONES to avoid feedback loops!")

with sd.Stream(channels=1, samplerate=FS, blocksize=CHUNK_SIZE, callback=audio_callback):
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("\nStopping...")
