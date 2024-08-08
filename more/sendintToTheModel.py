import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np



def predict_class_for_image(model_path, img_path):
    # Check if model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    # Load the trained model
    model = load_model(model_path)

    # Function to preprocess the image
    def preprocess_image(img_path, target_size=(224, 224)):
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array

    # Function to predict class for the image
    def predict_image_class(model, img_path):
        img = preprocess_image(img_path)
        predictions = model.predict(img)
        return predictions[0]  # Since we have only one image, return the first prediction

    # Check if image file exists
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image file not found at {img_path}")

    # Predict class for the image
    predictions = predict_image_class(model, img_path)

    # Determine the predicted class
    predicted_class = np.argmax(predictions)
    class_labels = ['yes', 'no']
    predicted_class_label = class_labels[predicted_class]

    return predicted_class_label

# Example usage
if __name__ == "__main__":
    model_path = 'back end - python/saved_models/vgg16-middlePart_yea_no.h5'  # Replace with your model path
    img_path = 'back end - python/ '    # Replace with your image path

    predicted_class = predict_class_for_image(model_path, img_path)
    print(f"Predicted class for the image: {predicted_class}")





























# # Specify the path to the saved model
# model_path = 'build vgg16/running_on_200/vgg16-middlePart_run_on_200.h5'

# # Ensure the file exists before loading
# if not os.path.exists(model_path):
#     raise FileNotFoundError(f"Model file not found at {model_path}")

# # Load the trained model
# model = load_model(model_path)

# # Function to load and preprocess the image
# def load_and_preprocess_image(img_path, target_size=(224, 224)):
#     img = image.load_img(img_path, target_size=target_size)
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     print(img_array.shape)
#     return img_array

# def predict_image(model, img_path):
#     img = load_and_preprocess_image(img_path)
#     predictions = model.predict(img)
#     return predictions[0]  # Since we have only one image, return the first prediction

# # Example usage
# if __name__ == "__main__":
#     img_path = 'back end - python/03-02-2016-172812 asmix bugdorm _part1.png'  # Replace with your image path
#     if not os.path.exists(img_path):
#         raise FileNotFoundError(f"Image file not found at {img_path}")
    
#     predictions = predict_image(model, img_path)
#     print(f"Predictions: {predictions}")

#     predicted_class = np.argmax(predictions)
#     class_labels = ['yes', 'no']
#     print(f"Predicted class: {class_labels[predicted_class]}")
















# import tensorflow as tf
# import numpy as np
# from tensorflow.keras.preprocessing import image
# from keras.src.saving import load_model





# # Load the model (replace 'your_model.h5' with the path to your actual model file)
# model = tf.keras.models.load_model('build vgg16/running_on_200/vgg16-middlePart_run_on_200.h5')

# def sendToTheModel(spectrogram_image_path):
#     # Load the image
#     img = image.load_img(spectrogram_image_path, target_size=(224, 224))  # Adjust target_size to match your model's expected input size
#     # Convert the image to an array
#     img_array = image.img_to_array(img)
#     # Expand dimensions to match the shape the model expects (batch size, height, width, channels)
#     img_array = np.expand_dims(img_array, axis=0)
#     # Normalize the image
#     img_array /= 255.0

#     # Make a prediction
#     prediction = model.predict(img_array)
#     print("Im the model")
#     print(prediction)
#     # predicted_class = np.argmax(prediction)
#     # if predicted_class == 0:
#     #     result = "yes"
#     # else:
#     #     result = "no"

#     print(f"Predicted Class: {result}")

# if __name__ == '__main__':
#     sendToTheModel('back end - python/03-03-2016-153338AfarM.png')
# # app.run(debug=True)