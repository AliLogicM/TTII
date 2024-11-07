from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.utils.process_video import process_frames
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected video'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extraer los frames del video
        process_frames(file_path, current_app.config['FRAMES_FOLDER'])

        return jsonify({'message': 'Video uploaded successfully'}), 200