import os
import pathlib
from os import terminal_size

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from keras import models
from jupyterlab import commands
from IPython import display
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras import layers
from tensorflow.python.data import AUTOTUNE
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

batch_size = 32
image_size = (224, 224)
classes = ['yes', 'no']

train_batches = ImageDataGenerator().flow_from_directory(
    directory='./data/pics/train',
    classes=classes,
    class_mode='categorical',
    target_size=image_size,
    batch_size=batch_size,
    shuffle=True
)

test_batches = ImageDataGenerator().flow_from_directory(
    directory='./data/pics/test',
    classes=classes,
    class_mode='categorical',
    target_size=image_size,
    batch_size=batch_size,
    shuffle=True
)



batch_size = 32
input_shape = (224,224,3)
num_labels = 2
norm_layer = layers.Normalization()

model = models.Sequential([
    layers.Input(shape=input_shape),
    layers.Conv2D(32, 3, activation='relu'),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_labels,activation='softmax'),
])

model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

EPOCHS = 15
history = model.fit(
    train_batches,
    validation_data=test_batches,
    epochs=EPOCHS,
    callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=4)
)

# Plot loss
metrics = history.history
plt.plot(metrics['loss'],'bo-',label='loss')
plt.plot(metrics['val_loss'],'ro-',label='val_loss')
#plt.xticks(range(0,15))
plt.xlabel('Number of epochs')

plt.show()

plt.plot(metrics['accuracy'],'go-',label='accuracy')
plt.plot(metrics['val_accuracy'],'ko-',label='val_accuracy')
#plt.xticks(range(0,15))
plt.xlabel('Number of epochs')
plt.show()


#####################################
predictions = model.predict(test_batches, steps=len(test_batches), verbose=1)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = test_batches.classes
conf_matrix = confusion_matrix(true_classes, predicted_classes)
cm_display = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=classes)
cm_display.plot(cmap=plt.cm.Blues)  # Optionally, use a color map for better visualization
plt.title('Confusion Matrix')
plt.savefig("cm_margin_50.png")  # Ensure the file extension is included
plt.show()
#####################################




# Evaluate model
test_audio = []
test_labels = []

for audio, label in test_batches:
    test_audio.append(audio) 
    test_labels.append(label)  

test_audio = np.array(test_audio)
test_labels = np.array(test_labels)

y_pred = np.argmax(model.predict(test_audio), axis=1)
y_true = np.argmax(test_labels, axis=1)

test_acc = sum(y_pred == y_true) / len(y_true)
print(f'Test set accuracy: {test_acc:.0%}')

# Plot confusion matrix
confusion_mtx = tf.math.confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_mtx,
            xticklabels=classes,
            yticklabels=classes,
            annot=True, fmt='g')
plt.xlabel('Prediction')
plt.ylabel('Label')
plt.show()


