# python-sounddevice
# python-sounddevice allows you to record audio from your microphone
# and store it as a NumPy array. This is a handy datatype for sound processing that
# can be converted to WAV format for storage using the scipy.io.wavfile module.
# Make sure to install the scipy module for the
# following example (pip install scipy).
# This automatically installs NumPy as one of its dependencies:

#לבדוק על מחשב בבית
import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file



#chat gpt:
import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # קצב דגימה
seconds = 3 # משך ההקלטה

try:
    # ביצוע ההקלטה
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print("מתחיל בהקלטה...")
    sd.wait()  # המתנה עד שההקלטה תסתיים

    # בדיקה שההקלטה התבצעה בהצלחה וכי תקלות לא התרחשו
    if len(myrecording) < int(seconds * fs):
        raise Exception("תקלה בהקלטת קול - לא הצלחנו להקליט את הקול כראוי")

    # שמירת ההקלטה כקובץ WAV
    write('output.wav', fs, myrecording)
    print("ההקלטה הושמרה בהצלחה.")
except Exception as e:
    print("שגיאה:", e)


# pyaudio
# Earlier in this article, you learned how to play
# sounds by reading a pyaudio.Stream().
# Recording audio can be done by writing to this stream instead:

import pyaudio
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()


# Saving and Converting Audio
# You saw earlier that you can use the scipy.io.wavfile
# module to store NumPy arrays as WAV files. The wavio module similarly
# lets you convert between WAV files and NumPy arrays. If you want to store
# your audio in a different file format, pydub and soundfile come in handy, as they allow you to read
# and write a range of popular file formats (such as MP3, FLAC, WMA and FLV).
#
# wavio
# This module depends on numpy and lets you read WAV files as NumPy arrays, and save NumPy arrays as WAV files.
#
#1
import wavio

wavio.write("myfile.wav", my_np_array, fs, sampwidth=2)

#2
import soundfile as sf

# Extract audio data and sampling rate from file
data, fs = sf.read('myfile.wav')
# Save as FLAC file at correct sampling rate
sf.write('myfile.flac', data, fs)





