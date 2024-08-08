import os
from pydub import AudioSegment

def mix_audio_with_reference(input_folder, reference_audio_file, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load the reference audio file
    reference_audio = AudioSegment.from_file(reference_audio_file)

    # Get the duration of the reference audio file
    reference_duration = len(reference_audio)

    # List all audio files in the input folder
    audio_files = [f for f in os.listdir(input_folder) if f.endswith('.wav') or f.endswith('.mp3')]

    # Iterate through each audio file in the input folder
    for file_name in audio_files:
        # Load the current audio file from the input folder
        audio_file_path = os.path.join(input_folder, file_name)
        current_audio = AudioSegment.from_file(audio_file_path)

        # Get the duration of the current audio file
        current_duration = len(current_audio)

        # Calculate the number of repetitions needed for the reference audio to match the duration of the current audio
        repetitions = current_duration // reference_duration + 1

        # Repeat the reference audio to match the duration of the current audio
        repeated_reference = reference_audio * repetitions

        # Concatenate the repeated reference audio with the current audio
        mixed_audio = current_audio.overlay(repeated_reference[:current_duration])

        # Save the mixed audio to the output folder
        output_file_path = os.path.join(output_folder, f"mixed_{file_name}")
        mixed_audio.export(output_file_path, format="mp3")

        print(f"Mixed {file_name} with reference audio and saved to {output_file_path}")

# Example usage:
input_folder = "build the model/more_data/new_audio/no"
reference_audio_file = "build the model/more_data/new_audio/Voice0165.wav"
output_folder = "build the model/more_data/new_audio/yes"
mix_audio_with_reference(input_folder, reference_audio_file, output_folder)





