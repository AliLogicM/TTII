from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Lógica para procesar el video y analizar emociones
    return jsonify({"message": "Análisis completado"})

if __name__ == '__main__':
    app.run(debug=True)
