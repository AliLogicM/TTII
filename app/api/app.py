from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configurar el directorio donde se guardarán los archivos subidos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['video']

    # Si el usuario no selecciona un archivo, el navegador también
    # puede enviar una parte vacía sin nombre de archivo.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "path": file_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
