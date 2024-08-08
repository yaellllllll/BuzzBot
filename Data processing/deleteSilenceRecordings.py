import os
from pydub import AudioSegment

def is_silent(audio_file, silence_threshold=-50.0, chunk_size=10):
    try:
        audio = AudioSegment.from_file(audio_file)
        audio = audio.set_channels(1)
        for i in range(0, len(audio), chunk_size):
            chunk = audio[i:i+chunk_size]
            if chunk.dBFS > silence_threshold:
                return False
        
        return True
    except Exception as e:
        print(f"Error processing {audio_file}: {e}")
        return False

def remove_silent_files(directory, silence_threshold=-50.0, chunk_size=10):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if is_silent(file_path, silence_threshold, chunk_size):
                os.remove(file_path)
                print(f"Removed silent file: {file_path}")




directory = "audio files/הקלטות מחולצות של הייתושים/Aedes aegypti"
remove_silent_files(directory)
