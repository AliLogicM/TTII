import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from app.utils.process_video import process_frames
from app.utils.emotion_detector import detect_emotions
from app.utils.risk_evaluation import assess_risk
from flask_sqlalchemy import SQLAlchemy
from app.models.dbModel import db, Results
from app import create_app

app = create_app()

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

# Verificar la conexión a la base de datos
@app.route('/get-results', methods=['GET'])
def get_results():
    try:
        # Consultar todos los registros en la tabla results
        results = Results.query.all()
        results_list = [{
            'id': result.id,
            'video_id': result.video_id,
            'emotions': result.emotions,
            'risk_assessment': result.risk_assessment,
            'created_at': result.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for result in results]
        
        return jsonify(results_list)
    except Exception as e:
        return jsonify({'status': 'Failed', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)