import os
import cv2
import numpy as np
import pandas as pd
import shutil
import random
import matplotlib.pyplot as plt
from collections import Counter, deque
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Input, Activation
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, f1_score, classification_report


# Configuración general
DATASET_DIR = "C:/Users/yaelo/OneDrive/Escritorio/TTII/Facial"  # Ruta base donde está el dataset CK+
OUTPUT_DIR = "C:/Users/yaelo/OneDrive/Escritorio/TTII/output"  # Carpeta para guardar el modelo y resultados
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuración de emociones
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']


# ------------------------- PREPARACIÓN DE LOS DATOS -------------------------

def process_images(folder):
    """Procesa las imágenes y las etiquetas desde el dataset."""
    processed_data = []
    labels = []
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for emotion in os.listdir(folder):
        emotion_path = os.path.join(folder, emotion)
        if not os.path.isdir(emotion_path):
            continue

        print(f"Procesando imágenes para la emoción: {emotion}")
        for img_name in os.listdir(emotion_path):
            img_path = os.path.join(emotion_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            # Detección facial
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                roi = img[y:y+h, x:x+w]
                roi_resized = cv2.resize(roi, (48, 48))  # Redimensionar a 48x48
                processed_data.append(roi_resized)
                labels.append(emotion)
    return np.array(processed_data), labels

# Procesar las carpetas de entrenamiento y validación
train_folder = os.path.join(DATASET_DIR, "train")
val_folder = os.path.join(DATASET_DIR, "validation")
train_data, train_labels = process_images(train_folder)
val_data, val_labels = process_images(val_folder)

# Guardar los datos procesados
np.save(os.path.join(OUTPUT_DIR, "train_data.npy"), train_data)
np.save(os.path.join(OUTPUT_DIR, "train_labels.npy"), train_labels)
np.save(os.path.join(OUTPUT_DIR, "val_data.npy"), val_data)
np.save(os.path.join(OUTPUT_DIR, "val_labels.npy"), val_labels)

print("Datos procesados y guardados correctamente.")

# ------------------------- PREPROCESAMIENTO -------------------------

# Normalizar las imágenes y codificar etiquetas
train_data = train_data / 255.0
val_data = val_data / 255.0

label_encoder = LabelEncoder()
train_labels_encoded = label_encoder.fit_transform(train_labels)
val_labels_encoded = label_encoder.transform(val_labels)

train_labels_categorical = to_categorical(train_labels_encoded, num_classes=len(emotion_labels))
val_labels_categorical = to_categorical(val_labels_encoded, num_classes=len(emotion_labels))

print(f"Etiquetas procesadas: {label_encoder.classes_}")

# ------------------------- DEFINICIÓN DEL MODELO -------------------------


# Definición del modelo
input = Input(shape=(48, 48, 1))  # Input de imágenes escala de grises

conv1 = Conv2D(32, (3, 3), padding='same', kernel_regularizer=l2(0.001))(input)
conv1 = Activation('relu')(conv1)
conv1 = MaxPooling2D(pool_size=(2, 2))(conv1)
conv1 = Dropout(0.1)(conv1)

conv2 = Conv2D(64, (3, 3), padding='same', kernel_regularizer=l2(0.001))(conv1)
conv2 = Activation('relu')(conv2)
conv2 = MaxPooling2D(pool_size=(2, 2))(conv2)
conv2 = Dropout(0.1)(conv2)

conv3 = Conv2D(128, (3, 3), padding='same', kernel_regularizer=l2(0.001))(conv2)
conv3 = Activation('relu')(conv3)
conv3 = MaxPooling2D(pool_size=(2, 2))(conv3)
conv3 = Dropout(0.1)(conv3)

conv4 = Conv2D(256, (3, 3), padding='same', kernel_regularizer=l2(0.001))(conv3)
conv4 = Activation('relu')(conv4)
conv4 = MaxPooling2D(pool_size=(2, 2))(conv4)  # Dropout movido después del MaxPooling
conv4 = Dropout(0.1)(conv4)

flatten = Flatten()(conv4)  # Asegúrate de que aquí se pase un tensor válido

dense_1 = Dense(128, activation='relu')(flatten)
drop_1 = Dropout(0.2)(dense_1)

output = Dense(len(emotion_labels), activation='softmax')(drop_1)

# Construcción y compilación del modelo
model = Model(inputs=input, outputs=output)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

# Configurar el guardado del modelo
model_path = os.path.join(OUTPUT_DIR, "emotion_model.h5")
checkpointer = ModelCheckpoint(
    model_path, monitor='val_loss', verbose=1, save_best_only=True, mode='h5'
)

# Entrenar el modelo
model.fit(
    train_data[..., np.newaxis],  # Agregar canal para escala de grises
    train_labels_categorical,
    batch_size=32,
    validation_data=(val_data[..., np.newaxis], val_labels_categorical),
    epochs=50,
    callbacks=[checkpointer]
)

print(f"Modelo entrenado y guardado en {model_path}")

val_loss, val_accuracy = model.evaluate(val_data[..., np.newaxis], val_labels_categorical)
print(f"Pérdida en validación: {val_loss:.4f}, Precisión en validación: {val_accuracy:.4f}")

def download_model_local(model_path, destination='./emotion_model_downloaded.h5'):
    """
    Copia el modelo entrenado a una ubicación específica para facilitar su descarga o transferencia.
    """
    if os.path.exists(model_path):
        shutil.copy(model_path, destination)
        print(f"Modelo copiado a: {destination}")
    else:
        print(f"El modelo no se encuentra en la ruta: {model_path}")

download_model_local('./output/emotion_model.h5', './emotion_model_downloaded.h5')

# ------------------------- DEFINICIÓN DEL MODELO -------------------------

# Configuración de emociones
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
NEGATIVE_EMOTIONS = ['angry', 'sad', 'fear', 'surprise']
POSITIVE_EMOTIONS = ['happy']
NEUTRAL_EMOTIONS = ['neutral', 'disgust']

# Parámetros para análisis de emociones
CHANGE_INTERVAL = 1
NEGATIVE_DURATION_THRESHOLD = 3
SEQUENTIAL_INTERVAL = 2
TOTAL_NEGATIVE_THRESHOLD = 10
FREQUENT_CHANGES_THRESHOLD = 5
RECURRING_THRESHOLD = 3

# Cargar el modelo entrenado
model_path = "C:/Users/yaelo/OneDrive/Escritorio/TTII/output/emotion_model.h5"
emotion_model = load_model(model_path)

# Buffer para almacenar emociones detectadas
emotion_history = deque(maxlen=60)

# Función para preprocesar un frame antes de pasarlo al modelo
def preprocess_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (48, 48))  # Redimensionar a 48x48
    normalized_frame = resized_frame / 255.0  # Normalizar
    return normalized_frame.reshape(1, 48, 48, 1)  # Expandir dimensiones para el modelo

# Función para detectar emociones en un frame
def detect_emotion(frame):
    preprocessed_frame = preprocess_frame(frame)
    prediction = emotion_model.predict(preprocessed_frame, verbose=0)
    return emotion_labels[np.argmax(prediction)]

# Funciones para las reglas (como antes)
def detect_rapid_changes(emotion_history):
    if len(emotion_history) < 2:
        return False
    recent_emotions = list(emotion_history)[-2:]
    time_diff = recent_emotions[1]['timestamp'] - recent_emotions[0]['timestamp']
    if time_diff <= CHANGE_INTERVAL and recent_emotions[0]['emotion'] != recent_emotions[1]['emotion']:
        return True
    return False

def detect_negative_sustained(emotion_history):
    negative_count = 0
    for record in reversed(emotion_history):
        if record['emotion'] in NEGATIVE_EMOTIONS:
            negative_count += 1
            if negative_count >= NEGATIVE_DURATION_THRESHOLD:
                return True
        else:
            break
    return False

def detect_sequential_emotions(emotion_history):
    if len(emotion_history) < 2:
        return False
    for i in range(len(emotion_history) - 1):
        if (
            emotion_history[i]['emotion'] in NEGATIVE_EMOTIONS
            and emotion_history[i + 1]['emotion'] in NEGATIVE_EMOTIONS
            and emotion_history[i + 1]['timestamp'] - emotion_history[i]['timestamp'] <= SEQUENTIAL_INTERVAL
        ):
            return True
    return False

def detect_total_negative_time(emotion_history):
    total_negative_time = sum(1 for record in emotion_history if record['emotion'] in NEGATIVE_EMOTIONS)
    return total_negative_time >= TOTAL_NEGATIVE_THRESHOLD

def detect_frequent_changes(emotion_history):
    if len(emotion_history) < 2:
        return False
    changes = sum(1 for i in range(1, len(emotion_history)) if emotion_history[i]['emotion'] != emotion_history[i - 1]['emotion'])
    return changes >= FREQUENT_CHANGES_THRESHOLD

def detect_recurring_negative_emotions(emotion_history):
    counter = Counter(record['emotion'] for record in emotion_history if record['emotion'] in NEGATIVE_EMOTIONS)
    for emotion, count in counter.items():
        if count >= RECURRING_THRESHOLD:
            return True
    return False

# Procesar un video para analizar emociones
def process_video(video_path, output_folder):
    # Extraer frames del video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / 10)  # Capturar 10 frames por segundo

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            detected_emotion = detect_emotion(frame)
            timestamp = len(emotion_history) + 1
            emotion_history.append({'emotion': detected_emotion, 'timestamp': timestamp, 'frame': frame})

            # Evaluar reglas
            if detect_rapid_changes(emotion_history):
                print(f"[{timestamp}s] Alerta: Cambio brusco de emociones detectado.")
            if detect_negative_sustained(emotion_history):
                print(f"[{timestamp}s] Alerta: Emoción negativa sostenida detectada.")
            if detect_sequential_emotions(emotion_history):
                print(f"[{timestamp}s] Alerta: Secuencia de emociones negativas detectada.")
            if detect_total_negative_time(emotion_history):
                print(f"[{timestamp}s] Alerta: Duración total de emociones negativas excedida.")
            if detect_frequent_changes(emotion_history):
                print(f"[{timestamp}s] Alerta: Frecuencia alta de cambios de emociones detectada.")
            if detect_recurring_negative_emotions(emotion_history):
                print(f"[{timestamp}s] Alerta: Emociones negativas recurrentes detectadas.")

        frame_count += 1

    cap.release()
    print("Procesamiento de video completado.")

# Ejecución
video_path = "C:/Users/yaelo/OneDrive/Escritorio/ProyectoTT/TTII/uploads/Prueba2.mp4"
output_folder = "C:/Users/yaelo/OneDrive/Escritorio/ProyectoTT/TTII/uploads/frames"
process_video(video_path, output_folder)

# Variables para recopilar estadísticas de evaluación
change_timestamps = []  # Marcas de tiempo de cambios bruscos
negative_durations = []  # Duración acumulada de emociones negativas
emotion_counts = Counter()  # Conteo de emociones detectadas
images_with_emotions = []  # Almacenar frames y emociones para visualización aleatoria

# Simular la recopilación de estadísticas durante el análisis
for record in emotion_history:
    timestamp = record['timestamp']
    emotion = record['emotion']
    emotion_counts[emotion] += 1
    if emotion in NEGATIVE_EMOTIONS:
        negative_durations.append(timestamp)
    if detect_rapid_changes(emotion_history):
        change_timestamps.append(timestamp)

    # Guardar aleatoriamente imágenes con emociones detectadas
    if random.random() < 0.1:  # Guardar un 10% de los frames
        images_with_emotions.append((record['frame'], emotion))

# Gráfica 1: Frecuencia de emociones detectadas
def plot_emotion_frequency(emotion_counts):
    plt.figure(figsize=(10, 6))
    plt.bar(emotion_counts.keys(), emotion_counts.values())
    plt.title("Frecuencia de Emociones Detectadas")
    plt.xlabel("Emoción")
    plt.ylabel("Frecuencia")
    plt.show()

# Gráfica 2: Cambios bruscos de emociones
def plot_rapid_changes(change_timestamps):
    plt.figure(figsize=(10, 6))
    plt.hist(change_timestamps, bins=10, color='orange')
    plt.title("Cambios Bruscos de Emociones")
    plt.xlabel("Tiempos (s)")
    plt.ylabel("Cantidad de Cambios")
    plt.show()

# Gráfica 3: Recurrencia de emociones negativas
def plot_negative_emotions(negative_durations):
    plt.figure(figsize=(10, 6))
    plt.hist(negative_durations, bins=10, color='red')
    plt.title("Recurrencia de Emociones Negativas")
    plt.xlabel("Tiempos (s)")
    plt.ylabel("Duración Acumulada (s)")
    plt.show()

# Mostrar una imagen aleatoria con emoción detectada
def show_random_image(images_with_emotions):
    if not images_with_emotions:
        print("No hay imágenes para mostrar.")
        return
    frame, emotion = random.choice(images_with_emotions)
    plt.figure(figsize=(6, 6))
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title(f"Emoción Detectada: {emotion}")
    plt.axis('off')
    plt.show()

# Llamar a las funciones para mostrar las visualizaciones
plot_emotion_frequency(emotion_counts)
plot_rapid_changes(change_timestamps)
plot_negative_emotions(negative_durations)
show_random_image(images_with_emotions)