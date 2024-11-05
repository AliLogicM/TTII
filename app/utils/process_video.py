import cv2
import os

def process_image(img):
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Normalización de la imagen
    normalized_img = cv2.normalize(gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # Redimensionar la imagen a un tamaño estándar (ejemplo: 48x48)
    resized_img = cv2.resize(normalized_img, (48, 48), interpolation=cv2.INTER_AREA)

    return resized_img

def process_frames(video_path, upload_folder):
    # Obtener el nombre del archivo de video sin la extensión
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(upload_folder, video_name)

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Capturar el video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    # Obtener la tasa de fotogramas (FPS) del video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / 10)  # Intervalo de frames para capturar 10 imágenes por segundo

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Guardar el frame si es el correspondiente al intervalo de 1/10 de segundo
        if frame_count % frame_interval == 0:
            processed_frame = process_image(frame)
            frame_filename = os.path.join(output_folder, f"frame_{frame_count // frame_interval:04d}.jpg")
            cv2.imwrite(frame_filename, processed_frame * 255)  # Multiplicar por 255 para convertir a rango [0, 255]

        frame_count += 1

    # Liberar el objeto de captura de video
    cap.release()
    print(f"Extracción completada. {frame_count // frame_interval} frames guardados en {output_folder}")