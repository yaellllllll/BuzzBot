import os
from tkinter import Image
from flask import Flask,request
import json
from flask import jsonify
from keras.src.saving import load_model
# from tensorflow.keras.preprocessing import image
# import tensorflow_model_optimization as tfmot
import tensorflow as tf  
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
from pydub import AudioSegment
import math
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np


app = Flask(__name__)

model = tf.keras.models.load_model('build vgg16/running_on_200/vgg16-middlePart_run_on_200.h5')


# פונקציה שמקבלת מהריאקט קובץ JSON של נתיני משתמש ומכניסה אותם לקובץ users.json בפייתון
@app.route('/homePage')
def homePage():
    return 'this is the home page'


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    with open('users.json', 'a') as file:
        file.write(",")
        json.dump(data, file)  # כתיבת נתוני המשתמש לקובץ JSON
        file.write('\n')  # הוספת שורה חדשה לסיום כל רשומה
    return 'נתוני המשתמש נוספו בהצלחה'


#פונקציה שמקבלת תז של משתמש ובודקת האם הוא קיים במערכת
@app.route('/findById/<user_id>', methods=['GET'])
def find_user_by_id(user_id):
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
        for user in data:
            if "id" in user and user["id"] == int(user_id):
                return jsonify({"user_found": True}), 200
        return jsonify({"user_found": False}), 404
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500


#פונקציה שמקבלת זן של היתוש ובודקת אם זה מסומן למשתמש במערך של ההתראות
#את ה ID של המשתמש הוא יצטרך לקבל מאנשוא שזה יישמר כמשתנה סביבה או משו
@app.route('/isExistMosquito/<user_id>/<name_mosquito>', methods=['GET'])
def check_if_exist_mosquito(user_id, name_mosquito):
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
        for user in data:
            if "id" in user and user["id"] == int(user_id):
                for m in user["mosquito"]:
                    if m == name_mosquito:
                        return jsonify({"mosquito_found": True}), 200
        return jsonify({"mosquito_found": False}), 404
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500
    

def get_volume_level(audio_file_path):
    print("Im in the volume function")
    try:
        print("should print detzibels")
        audio = AudioSegment.from_file(audio_file_path)
        # קביעת רמת רגישות - ניתן לשנות את הערך לפי הצורך
        sensitivity = 0.5
        # חישוב הווליום בדציבלים
        volume_db = audio.dBFS
        print(volume_db)
        if volume_db > -20:
            print("high")
            return "hige"
        elif volume_db > -30:
            print("high")
            return "middle"
        else:
            print("low")
            return "low"
    except Exception as e:
        print(" there is an error:", e)
        return None



#פונ שמקבלת ספקטוגרמה וחותכת אותה לגודל מדויק בלי המסגרת והבר צבעים
def crop_image(image_path, output_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            left = int(width * 0.08)  # 8% from the left
            top = int(height * 0.06)  # 6% from the top
            right = width - int(width * 0.20)  # 20% from the right
            bottom = height - int(height * 0.09)  # 9% from the bottom

            cropped_img = img.crop((left, top, right, bottom))
            cropped_img.save(output_path)
            print(f"Cropped image saved to: {output_path}")
    except Exception as e:
        print(f"Error cropping the image: {e}")

# פונ שמקבלת הקלטה והופכת אותה לספקטוגרמה ושולחת אותה לחתיכה
def change_to_spectogram(recording_data, output_directory, filename='recording', model=None):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    try:
        print("im in function spectograma")
        y, sr = librosa.load(recording_data, sr=None)
        D = librosa.stft(y)
        magnitude, _ = librosa.magphase(D)
        magnitude_db = librosa.amplitude_to_db(magnitude)
        temp_output_file_path = os.path.join(output_directory, f"{filename}_temp2.png")
        final_output_file_path = os.path.join(output_directory, f"{filename}.png")

        plt.figure(figsize=(10, 6))
        librosa.display.specshow(magnitude_db, sr=sr, x_axis='time', y_axis='log', vmin=-80, vmax=+80, cmap=cm.magma)
        plt.title('Spectrogram')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.savefig(temp_output_file_path)
        plt.close()
        
        crop_image(temp_output_file_path, final_output_file_path)
        os.remove(temp_output_file_path)
        
        print('model is existed')
        # img = Image.open(final_output_file_path).convert('RGB')
        # img = img.resize((224, 224))  # Resize as per your model's input size
        # img_array = np.array(img) / 255.0  # Normalize the image
        # img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension  
        # prediction = model.predict(img_array)
        # print(f"Prediction: {prediction}!!!!!!!!!*******")
        print("Im going to send it the model")
        sendToTheModel(final_output_file_path)

        return final_output_file_path
    except Exception as e:
        print(f"Error processing the recording: {e}")
        return None


@app.route('/getRecording', methods=['POST'])
def getRecording():
    print("hi Iam in get recording!!!")
    if 'recording' not in request.files:
        return 'No recording file found', 400
    recording_file = request.files['recording']
    recording_file_path = 'back end - python/save the recording/recording.wav'  # Update this with the path where you save the recording file
    recording_file.save(recording_file_path) 
    print("send to the volume function")
    volume_of_the_recording = get_volume_level(recording_file_path)
    print(volume_of_the_recording)  # Print the volume of the recording
    output_file_path = change_to_spectogram(recording_file_path, 'spectograms', 'my_recording')
    if output_file_path:
        return f'Spectrogram generated successfully: {output_file_path}', 200
    else:
        return 'Error generating spectrogram', 500



def sendToTheModel(spectrogram_image_path):
    # Load the image
    print("Im in the model")
    img = image.load_img(spectrogram_image_path, target_size=(224, 224))  # Adjust target_size to match your model's expected input size
    # Convert the image to an array
    img_array = image.img_to_array(img)
    # Expand dimensions to match the shape the model expects (batch size, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)
    # Make a prediction
    prediction = model.predict(img_array)
    print("Im the model")
    print(prediction)
    predicted_class = np.argmax(prediction)
    if predicted_class == 0:
        result = "yes"
    else:
        result = "no"

    print(f"Predicted Class: {result}")
    return result










if __name__ == '__main__':
    app.run(debug=True)
    sendToTheModel('back end - python/03-03-2016-153338AfarM.png')


