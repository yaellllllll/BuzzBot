from pydub import utils, AudioSegment


def get_prober_name():
    return r"C:\ffmpeg-master-latest-win64-gpl-shared\bin\ffprobe.exe"


AudioSegment.converter = r"C:\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
utils.get_prober_name = get_prober_name
#sound = AudioSegment.from_mp3("test.mp3")


def cut_audio_to_one_minute(input_file, output_prefix):
    AudioSegment.converter = r"C:\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"

    # טעינת הקובץ הקיים
    audio = AudioSegment.from_mp3(input_file)

    # מקצה הקובץ למספר קבצים באורך של דקה
    one_minute = 60 * 1000  # במילישניות
    num_slices = len(audio) // one_minute

    for i in range(num_slices):
        # חיתוך הקובץ לדקה
        slice_start = i * one_minute
        slice_end = (i + 1) * one_minute
        sliced_audio = audio[slice_start:slice_end]

        # שמירת הקובץ החתוך
        output_file = f"{output_prefix}_{i + 15}.wav"
        sliced_audio.export(output_file, format="wav")

if __name__ == "__main__":
    input_file = r"another long ramdom audiov/הרצאות הורים_ התמודדות בשעת משבר 16_10 (128kbps).mp3"
    output_prefix = "cuted random recordings 2"
    cut_audio_to_one_minute(input_file, output_prefix)


