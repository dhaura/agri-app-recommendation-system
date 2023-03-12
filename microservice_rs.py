import os

from flask import Flask, jsonify, request
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

import config

app = Flask(__name__)

DEFAULT_HEADERS = {"Content-Type": "application/json"}

disease_info = pd.read_csv('./feed/info/disease_info.csv', encoding='cp1252')

model = CNN.CNN(39)
model.load_state_dict(torch.load("./feed/plant_disease_model_latest.pt", map_location=torch.device('cpu')))
model.eval()


def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index


@app.route('/', methods=["GET"])
def health_check():
    payload = {
        "message": "Welcome to the example microservice recommendation system",
        "status": "success"
    }
    return jsonify(payload), 200, DEFAULT_HEADERS


@app.route('/predict_disease', methods=["POST"])
def predict_disease():
    sector = request.get_json()['sector']

    image_path = './feed/image_feed/sector_'+str(sector)+'.JPG'
    pred = prediction(image_path)

    payload = {
        "sector": str(sector),
        "condition": disease_info['disease_name'][pred],
        "possible-recommendations": disease_info['Possible Steps'][pred],
        "status": "success",
    }
    return jsonify(payload), 200, DEFAULT_HEADERS


if __name__ == "__main__":
    app.run(
        debug=config.DEBUG_MODE, host=config.MS_HOST, port=os.getenv('PORT', config.MS_PORT)
    )