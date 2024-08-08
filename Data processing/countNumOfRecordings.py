import os

def count_audio_files(directory, audio_extensions=None):
    """
    Counts the total number of audio files in the given directory, including subdirectories.
    
    Parameters:
    directory (str): Path to the directory to check.
    audio_extensions (list): List of audio file extensions to count. Default is common audio formats.
    
    Returns:
    int: Total number of audio files.
    """
    if audio_extensions is None:
        audio_extensions = ['.wav', '.mp3', '.flac', '.aac', '.ogg', '.wma', '.m4a']
    
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                count += 1

    return count

# Example usage
directory = "audio files/הקלטות מחולצות של הייתושים"
total_audio_files = count_audio_files(directory)
print(f"Total number of audio files: {total_audio_files}")
