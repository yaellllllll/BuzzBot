from pydub import AudioSegment


def cut_audio_into_sections():
    audio = AudioSegment.from_file('random recordings/first.mp3')

    # Define length of each section in milliseconds (1 minute)
    section_length_ms = 60000

    # Iterate over the sections
    for i in range(10):
        start_time = i * section_length_ms
        end_time = (i + 1) * section_length_ms
        segment = audio[start_time:end_time]

        # Construct output file path
        output_file_path = f"cut_random_recordings/section_{i + 1}.mp3"

        # Export segment to a file
        segment.export(output_file_path, format="mp3")


if __name__ == "__main__":
    cut_audio_into_sections()


