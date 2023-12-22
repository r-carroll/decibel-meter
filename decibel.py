import pyaudio
import time
import sqlite3
import numpy as np

def get_decibels():
    """Get the decibel levels from the microphone."""
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    data = stream.read(1024)
    stream.close()

    # Convert the audio data to float
    data = np.frombuffer(data, np.float32)

    # Convert the audio data to decibels
    amplitude = np.sqrt(np.mean(data**2))
    decibels = 20 * np.log10(amplitude)
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
