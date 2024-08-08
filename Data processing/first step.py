
import librosa
import matplotlib.pyplot as plt
import librosa.display
from scipy.io import wavfile
from IPython.display import Audio

from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt




#מצייר את האודיו פסים כאלה תכלת
# Read the Audiofile
samplerate, data = read('Voice0092.wav')
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

