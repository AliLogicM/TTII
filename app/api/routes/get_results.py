from flask import Blueprint, jsonify
from app.models.dbModel import Results

get_results_bp = Blueprint('get_results', __name__)

@get_results_bp.route('/get-results', methods=['GET'])
def get_results():
    results = Results.query.all()
    results_list = [{'id': result.id, 'data': result.data} for result in results]
    return jsonify(results_list)