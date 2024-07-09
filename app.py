# from flask import Flask, request, jsonify
# import os

# app = Flask(__name__)

# PERSISTENT_VOLUME_PATH = "/Naman_PV_dir"

# @app.route('/store-file', methods=['POST'])
# def store_file():
#     data = request.json
#     if not data or 'file' not in data or 'data' not in data:
#         return jsonify({"file": None, "error": "Invalid JSON input."}), 400

#     file_name = data['file']
#     file_data = data['data']

#     try:
#         with open(os.path.join(PERSISTENT_VOLUME_PATH, file_name), 'w') as f:
#             f.write(file_data)
#         return jsonify({"file": file_name, "message": "Success."})
#     except Exception as e:
#         return jsonify({"file": file_name, "error": str(e)}), 500

# @app.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.json
#     if not data or 'file' not in data or 'product' not in data:
#         return jsonify({"file": None, "error": "Invalid JSON input."}), 400

#     file_name = data['file']
#     product = data['product']

#     try:
#         with open(os.path.join(PERSISTENT_VOLUME_PATH, file_name), 'r') as f:
#             lines = f.readlines()
#         total = sum(int(line.split(',')[1]) for line in lines[1:] if line.split(',')[0] == product)
#         return jsonify({"file": file_name, "sum": total})
#     except FileNotFoundError:
#         return jsonify({"file": file_name, "error": "File not found."}), 404
#     except Exception as e:
#         return jsonify({"file": file_name, "error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
import os
import requests

# Reused my Assignment-1 code here.

from flask import Flask, request

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():

    # 1. Validate input JSON to ensure file name was provided
    try:
        if request.json["file"] == None:
            return {
                    "file": None,
                    "error": "Invalid JSON input."
                }
    except KeyError:
        return {
                    "file": None,
                    "error": "Invalid JSON input."
            }

    # 2. Verify that file exists
    if not os.path.isfile("/Naman_PV_dir/" + request.json["file"]):
        return {
            "file": request.json["file"],
            "error": "File not found."
            }


    # 3. Send the "file" and "product" parameters to container 2 and return response back.
    response = requests.post(url="http://container-2-service:8080/sum",json=request.json, headers={'Content-Type': 'application/json'})
    return response.json()

@app.route("/store-file", methods=["POST"])
def store_file():

    # 1. Validate input JSON to ensure file name was provided
    try:
        if request.json["file"] == None:
            return {
                    "file": None,
                    "error": "Invalid JSON input."
                }
    except KeyError:
        return {
                    "file": None,
                    "error": "Invalid JSON input."
            }

    # 2. Store the file.
    try:
        with open("/Naman_PV_dir/" + request.json["file"], "w+") as csvfile:
            csvfile.write(request.json["data"].replace(" ", ""))

    except Exception as e:
        # 2.1 Send error response if there was exception.
        return {
                    "file": None,
                    "error": "Error while storing the file to the storage."
            }
    # 2.2 Send success response if there was no exception during creating/storing the file.
    return {
        "file": request.json["file"],
        "message": "Success."
    }


if __name__ == "__main__":
    app.json.sort_keys = False
    app.run(host="0.0.0.0", port=8080, debug=True)
