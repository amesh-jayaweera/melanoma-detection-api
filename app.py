from flask import Flask, request, jsonify
from flask_cors import CORS
from melanoma_detection_pps import detect_melanoma_by_pps, Data
from melanoma_detection_dna import detect_mutations
from melanoma_detection_dermoscopic_images import checkMelanoma
import numpy as np
import cv2

app = Flask(__name__)
cors = CORS(app, resources={r"/predict-melanoma/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/predict-melanoma/pps', methods=['POST'])
def melanoma_detection_by_pps():
    try:
        data = request.get_json(force=True)
        input_data = Data(data['age'], data['gene'], data['tumor'], data['tier'], data['mutated_dna'])

        # passing data to module 2
        mutations, mutation_positions = detect_mutations(data['age'],data['mutated_dna'],data['gene'])
        if(len(mutations)!=0):
            # passing data to module 3
            output = detect_melanoma_by_pps(input_data)
            output.update({'mutations': mutations ,'mutation_positions':mutation_positions})
            response = jsonify(output)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200  # request completed successfully
        else:
            return null, 200  # request completed successfully, no mutations found
    except Exception as e:
        print(e)
        return {"message": "Something went wrong!"}, 400  # bad request


@app.route('/predict-melanoma/dermoscopic-images', methods=['POST'])
def melanoma_detection_by_dermoscopic_images():
    try:
        filestr = request.files['image'].read()
        npimg = np.fromstring(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        extension = request.files['image'].filename.split(".")[1]
        required_file_extensions = ['png', 'jpg', 'jpeg']
        if extension in required_file_extensions:
            output = checkMelanoma(img)
            response = jsonify(output)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200  # request completed successfully
        else:
            return "Bad request", 400
    except Exception as e:
        print(e)
        return "Bad request", 400  # bad request


if __name__ == "__main__":
    app.run()
