# Read audio
import soundfile as sf
import noisereduce as nr
import librosa
import IPython.display as ipd


data, samplerate = sf.read('Voice0091.wav')
# reduce noise
y_reduced_noise = nr.reduce_noise(y=data, sr=samplerate)
# save audio
sf.write('Vocals_reduced.wav', y_reduced_noise, samplerate, subtype="PCM_24")
# load and play audio
data, samplerate = librosa.load('Vocals_reduced.wav')
ipd.Audio('Vocals_reduced.wav')
