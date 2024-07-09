from flask import Flask, request, jsonify
import os

app = Flask(__name__)

PERSISTENT_VOLUME_PATH = "/Naman_PV_daair"

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.json
    if not data or 'file' not in data or 'data' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    file_data = data['data']

    try:
        with open(os.path.join(PERSISTENT_VOLUME_PATH, file_name), 'w') as f:
            f.write(file_data)
        return jsonify({"file": file_name, "message": "Success."})
    except Exception as e:
        return jsonify({"file": file_name, "error": str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    if not data or 'file' not in data or 'product' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data['product']

    try:
        with open(os.path.join(PERSISTENT_VOLUME_PATH, file_name), 'r') as f:
            lines = f.readlines()
        total = sum(int(line.split(',')[1]) for line in lines[1:] if line.split(',')[0] == product)
        return jsonify({"file": file_name, "sum": total})
    except FileNotFoundError:
        return jsonify({"file": file_name, "error": "File not found."}), 404
    except Exception as e:
        return jsonify({"file": file_name, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
