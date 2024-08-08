import os
from keras.src.ops import numpy
from matplotlib import pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D,Dropout,Flatten
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


batch_size = 32 #חלוקה לאצוות נתונים של 32 
image_size = (224, 224)
classes = ['yes','no']
#trainטעינת ערכת ה 
train_batches = ImageDataGenerator().flow_from_directory(
    directory='build the model/build vgg16/pics/train1',
    classes=classes,
    class_mode='categorical',
    target_size=image_size,
    batch_size=batch_size,
    shuffle=True
)
#test ערכת ה 
test_batches = ImageDataGenerator().flow_from_directory(
    directory='build the model/build vgg16/pics/test1',
    classes=classes,
    class_mode='categorical',
    target_size=image_size,
    batch_size=batch_size,
    shuffle=False
)

def build_vgg16():
 #vgg16 קו זה טוען את דגם  עם הפרמטרים הבאים:
#מוגדר לתמונות בגודל 224*224 על 3 ערוצי צבע
    vgg16_base = VGG16(input_shape=(224, 224, 3), include_top=True, weights='imagenet')
# חותך את הדגם  המקורי, ומסיר את השכבות המחוברות במלואן.
    vgg16_base = Model(inputs=vgg16_base.input, outputs=vgg16_base.get_layer('block5_pool').output)
#VGG16 מקפיא את כל השכבות בדגם הבסיס של  כדי להשתמש בו כמחלץ תכונות קבוע, 
#ומונע את עדכון המשקולות שלהם במהלך האימון.
    for layer in vgg16_base.layers:
        layer.trainable = False
#Fully Connected הקוד מוסיף שלוש שכבות  עם 4096 יחידות כל אחת,
#עם פונ רלו מופרדות בשכבות של דרופ 
#השכברה הראשונה משטחת כדי להתאים לשכבות הבאות
    x = Flatten()(vgg16_base.output)
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.25)(x)
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.25)(x)
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.25)(x)
    predictions = Dense(len(classes), activation='softmax')(x)

#מגדיר את המודל החדש ומחזיר אותו
    myModel = Model(inputs=vgg16_base.input, outputs=predictions)
    return myModel

def compile_model():
    model = build_vgg16()
#מגדיר פונקציית לוס, אופטימיזציה להתאמת המשקלות,ומדד דיוק
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
#מציג סיכום של המודל
    model.summary()
    return model

def fit_model():
    step_size_train = len(train_batches)
    step_size_valid = len(test_batches)
    model = compile_model()
    history = model.fit(train_batches,
                        epochs=20,
                        steps_per_epoch=step_size_train,
                        validation_data=test_batches,
                        validation_steps=step_size_valid,
                        verbose=1)

    step_size_test = len(test_batches)
    result = model.evaluate(test_batches, steps=step_size_test)
#שמירת המודל
    save_dir = os.path.join(os.getcwd(), 'build the model/build vgg16/saved_models')
    model_name = 'vgg16-middlePart_200_images.h5'
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
#הצגת מדדי הדיוק וההפסד בגרף ושמירה
    plt.figure(figsize=(10, 10))
    plt.plot(history.history['accuracy'], 'bo-', label='Train Accuracy - middle part vgg16')
    plt.plot(history.history['val_accuracy'], 'ro-', label='Test Accuracy - middle part vgg16')
    plt.xticks(range(0, 31))
    plt.xlabel('Number of epochs')
    plt.ylabel('Accuracy')
    plt.savefig("history_middlepart_16_2_3")
    plt.legend()

    print("Test set classification accuracy: {0:.2%}".format(result[1]))
    return history, model

if __name__ == "__main__":
    history, model = fit_model()
    predictions = model.predict(test_batches, steps=len(test_batches), verbose=1)
    predicted_classes = numpy.argmax(predictions, axis=1)
    true_classes = test_batches.classes

    # confusion matrix
    confusion_matrix = confusion_matrix(true_classes, predicted_classes)
    cm_display = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix)
    cm_display.plot()
    plt.savefig("cm_middlepart_16_200_images")
    plt.show()

