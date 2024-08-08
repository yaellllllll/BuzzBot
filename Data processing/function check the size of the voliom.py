

#בדקנו וזה עובד!!!!!!!!!


# כדי למדוד את עוצמת הווליום בקובץ שמע ולהחליט אם היא גבוהה, בינונית או נמוכה, נשתמש בספריית pydub בפייתון. נבצע את הצעדים הבאים:
#
# נתקין את הספרייה pydub באמצעות pip install pydub.
# נכתוב פונקציה שתקבל את הנתיב לקובץ שמע ותחזיר את עוצמת הווליום במילות "גבוהה", "בינונית" או "נמוכה".
# הנה קוד לפונקציה כזו:


from pydub import AudioSegment
import math

def get_volume_level(audio_file_path):
    try:
        audio = AudioSegment.from_file(audio_file_path)
        # קביעת רמת רגישות - ניתן לשנות את הערך לפי הצורך
        sensitivity = 0.5
        # חישוב הווליום בדציבלים
        volume_db = audio.dBFS
        if volume_db > -20:
            return "גבוהה"
        elif volume_db > -30:
            return "בינונית"
        else:
            return "נמוכה"
    except Exception as e:
        print("התרחשה שגיאה:", e)
        return None

# הפעלת הפונקציה עם הנתיב לקובץ שמע
audio_file_path = "Voice0092.wav"
volume_level = get_volume_level(audio_file_path)
if volume_level is not None:
    print("עוצמת הווליום היא:", volume_level)