##1

import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load audio file
audio_file = 'Voice0092.wav'
try:
    y, sr = librosa.load(audio_file)
except Exception as e:
    print("Error loading audio file:", e)
    exit()

# Compute STFT
D = librosa.stft(y)

# Get magnitudes
magnitude, phase = librosa.magphase(D)

# Convert to dB scale
magnitude_db = librosa.amplitude_to_db(magnitude)

# Visualize the spectrogram
plt.figure(figsize=(10, 6))
librosa.display.specshow(magnitude_db, sr=sr, x_axis='time', y_axis='log')
plt.title('Spectrogram')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()


##2
# Loading the Libraries
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt

# Read the Audiofile
samplerate, data = read('6TU5302374.wav')
# Frame rate for the Audio
print(samplerate)

# Duration of the audio in Seconds
duration = len(data)/samplerate
print("Duration of Audio in Seconds", duration)
print("Duration of Audio in Minutes", duration/60)

time = np.arange(0,duration,1/samplerate)

# Plotting the Graph using Matplotlib
plt.plot(time,data)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('6TU5302374.wav')
plt.show()