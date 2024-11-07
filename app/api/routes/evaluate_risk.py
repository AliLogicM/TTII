from flask import Blueprint, request, jsonify
from app.utils.risk_evaluation import assess_risk

evaluate_risk_bp = Blueprint('evaluate_risk', __name__)

@evaluate_risk_bp.route('/evaluate_risk', methods=['POST'])
def evaluate_risk():
    # Aquí puedes agregar lógica para extraer la imagen de la solicitud si es necesario
    result = assess_risk(None)  # Pasar el objeto de imagen adecuado
    return jsonify(result)