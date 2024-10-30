import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from app.utils.process_video import extract_frames  # Use relative import

app = Flask(__name__)

# Configura un directorio para los archivos cargados
UPLOAD_FOLDER = 'uploads/'
FRAMES_FOLDER = 'uploads/frames/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(FRAMES_FOLDER):
    os.makedirs(FRAMES_FOLDER)
    
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FRAMES_FOLDER'] = FRAMES_FOLDER



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

        # Extraer los frames del video
        extract_frames(file_path, app.config['FRAMES_FOLDER'])

        return jsonify({'message': 'Video uploaded successfully'}), 200
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)