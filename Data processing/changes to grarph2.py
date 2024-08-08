import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import glob
import matplotlib.cm as cm

def process_audio_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in glob.glob(os.path.join(input_directory, '*.mp3')) + glob.glob(os.path.join(input_directory, '*.wav')) + glob.glob(os.path.join(input_directory, '*.ogg')):
        print(f"Processing audio file: {filename}")
        try:
            y, sr = librosa.load(filename)
            D = librosa.stft(y)
            magnitude, _ = librosa.magphase(D)
            magnitude_db = librosa.amplitude_to_db(magnitude)

            output_file_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(filename))[0]}.png")

            plt.figure(figsize=(10, 6))
            librosa.display.specshow(magnitude_db, sr=sr, x_axis='time', y_axis='log', vmin=-80, vmax=+80, cmap=cm.magma)
            plt.title('Spectrogram')
            plt.colorbar(format='%+2.0f dB')
            plt.tight_layout()
            with open(output_file_path, 'wb') as out_file:
                plt.savefig(out_file)  # Save 
            plt.close()  

        except Exception as e:
            print(f"Error processing audio file {filename}: {e}")
            continue

input_dir = 'spectogram for the bag/audio'
output_dir = 'spectogram for the bag/image'
process_audio_files(input_dir, output_dir)

