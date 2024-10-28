import os
import cv2
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configura un directorio para los archivos cargados
UPLOAD_FOLDER = 'uploads/'
FRAMES_FOLDER = 'uploads/frames/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FRAMES_FOLDER'] = FRAMES_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(FRAMES_FOLDER):
    os.makedirs(FRAMES_FOLDER)

def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    return frame_count

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected video'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extraer frames del video cargado
        frames_output_folder = os.path.join(app.config['FRAMES_FOLDER'], filename.split('.')[0])
        frame_count = extract_frames(file_path, frames_output_folder)

        return jsonify({'message': 'Video uploaded and frames extracted successfully', 'path': file_path, 'frames': frame_count}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)