import pyaudio
import time
import sqlite3
import numpy as np

def get_decibels():
    """Get decibel levels from the Enviro Plus microphone."""
    pa = pyaudio.PyAudio()

    # Select Enviro Plus microphone (adjust index if needed)
    index = 4  # Assuming Enviro Plus mic is the third device
    info = pa.get_device_info_by_index(index)
    device_name = info['name']
    if "Enviro+" in device_name:
        print("Using Enviro Plus microphone:", device_name)
    else:
        print("Enviro Plus microphone not found!")
        return None

    # Open stream with potential adjustments
    stream = pa.open(format=pyaudio.paInt16,  # Try different audio format
                     channels=1,
                     rate=44100,
                     input=True,
                     input_device_index=index,
                     frames_per_buffer=1024)

    data = stream.read(1024)
    stream.close()

    # Convert audio data to decibels with A-weighting
    data = np.frombuffer(data, np.int16)  # Adjust for audio format
    amplitude = np.sqrt(np.mean(data**2))
    decibels = 20 * np.log10(amplitude)
    #decibels_weighted = apply_a_weighting(decibels)  # Apply A-weighting
    return decibels

def save_decibels(decibels):
    """Save the decibel levels to the database."""
    connection = sqlite3.connect("decibel_levels.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO decibel_levels (decibels) VALUES (?)", (decibels,))
    connection.commit()

def main():
    """The main function."""
    while True:
        decibels = get_decibels()
        print(decibels)
        #save_decibels(decibels)
        time.sleep(1)

if __name__ == "__main__":
    main()
