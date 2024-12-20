import cv2
import os

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
            frame_filename = os.path.join(output_folder, f"frame_{frame_count // frame_interval:04d}.jpg")
            cv2.imwrite(frame_filename, frame)  # Multiplicar por 255 para convertir a rango [0, 255]

        frame_count += 1

    # Liberar el objeto de captura de video
    cap.release()
    print(f"Extracción completada. {frame_count // frame_interval} frames guardados en {output_folder}")