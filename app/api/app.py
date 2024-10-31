import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from app.utils.process_video import process_frames
from app.utils.emotion_detector import detect_emotions
from app.utils.risk_evaluation import assess_risk

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
        process_frames(file_path, app.config['FRAMES_FOLDER'])

        return jsonify({'message': 'Video uploaded successfully'}), 200
    
@app.route('/detect-emotions', methods=['POST'])
def emotion_detector():
    # Aquí puedes agregar lógica para extraer la imagen de la solicitud si es necesario
    result = detect_emotions(None)  # Pasar el objeto de imagen adecuado
    return jsonify(result)

@app.route('/evaluate_risk', methods=['POST'])
def evaluate_risk():
    # Aquí puedes agregar lógica para extraer la imagen de la solicitud si es necesario
    result = assess_risk(None)  # Pasar el objeto de imagen adecuado
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)