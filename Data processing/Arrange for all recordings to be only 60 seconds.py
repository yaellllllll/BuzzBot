import os
from pydub import AudioSegment

def process_audio_files(folder_path):
    # List all files in the folder
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav') or f.endswith('.mp3') or f.endswith('.m4a') or f.endswith('.amr')]

    for file_name in audio_files:
        print(f"Processing file: {file_name}")  # Debugging output

        file_path = os.path.join(folder_path, file_name)
        try:
            audio = AudioSegment.from_file(file_path)
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue

        # Check the length of the audio file in seconds
        duration_seconds = len(audio) / 1000.0

        if duration_seconds < 60:
            # Delete the file if it's less than 60 seconds
            os.remove(file_path)
            print(f"Deleted {file_name} because it is less than 60 seconds.")
        else:
            # Split the file into chunks of 60 seconds
            chunk_length_ms = 60 * 1000  # 60 seconds in milliseconds
            chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

            # Save the chunks that are exactly 60 seconds
            for i, chunk in enumerate(chunks):
                if len(chunk) < chunk_length_ms:
                    # Skip chunks less than 60 seconds
                    print(f"Skipping chunk {i + 1} from {file_name} because it is less than 60 seconds.")
                    continue

                chunk_name = f"{os.path.splitext(file_name)[0]}_part{i + 1}.wav"
                chunk_path = os.path.join(folder_path, chunk_name)
                chunk.export(chunk_path, format="wav")
                print(f"Exported {chunk_name}")

if __name__ == "__main__":
    folder_path = "Anopheles dirus"
    process_audio_files(folder_path)
