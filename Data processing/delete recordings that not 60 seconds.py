import os
from pydub import AudioSegment

def process_audio_files(folder_path):
    # List all files in the folder
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav') 
                   or f.endswith('.mp3') or f.endswith('.m4a') or f.endswith('.amr')]
    for file_name in audio_files:
        print(f"Processing file: {file_name}")
        file_path = os.path.join(folder_path, file_name)
        try:
            audio = AudioSegment.from_file(file_path)
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue

        # Check the length 
        duration_seconds = len(audio) / 1000.0
        if duration_seconds < 60:
            os.remove(file_path)
            print(f"Deleted {file_name} because it is less than 60 seconds.")
        elif duration_seconds == 60:
            print(f"File {file_name} is exactly 60 seconds.")
        else:
            chunk_length_ms = 60 * 1000  # 60 seconds 
            chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
            # Remove 
            os.remove(file_path)
            print(f"Removed original file {file_name} as it is longer than 60 seconds.")
            # Save 
            for i, chunk in enumerate(chunks):
                if len(chunk) < chunk_length_ms:
                    print(f"Skipping chunk {i + 1} from {file_name} because it is less than 60 seconds.")
                    continue

                chunk_name = f"{os.path.splitext(file_name)[0]}_part{i + 1}.wav"
                chunk_path = os.path.join(folder_path, chunk_name)
                chunk.export(chunk_path, format="wav")
                print(f"Exported {chunk_name}")

if __name__ == "__main__":
    folder_path = 'build the model/more_data/audio/no'
    process_audio_files(folder_path)
