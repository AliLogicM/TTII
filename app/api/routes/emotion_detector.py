from flask import Blueprint, request, jsonify
from app.utils.emotion_detector import detect_emotions

emotion_detector_bp = Blueprint('emotion_detector', __name__)

@emotion_detector_bp.route('/detect-emotions', methods=['POST'])
def emotion_detector():
    # Aquí puedes agregar lógica para extraer la imagen de la solicitud si es necesario
    result = detect_emotions(None)  # Pasar el objeto de imagen adecuado
    return jsonify(result)