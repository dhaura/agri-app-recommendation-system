import os

from flask import Flask, request, jsonify
from flask import Flask, redirect, render_template, request
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

import config

app = Flask(__name__)

DEFAULT_HEADERS = {"Content-Type": "application/json"}

disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

model = CNN.CNN(39)
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
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

    image = request.files['image']
    image_path = 'image_feed/sector_'+str(sector)+'.jpg'
    pred = prediction(image_path)

    payload = {
        "message": str(pred),
        "status": "success",
        "sector": str(sector),
    }
    return jsonify(payload), 200, DEFAULT_HEADERS


if __name__ == "__main__":
    app.run(
        debug=config.DEBUG_MODE, host=config.MS_HOST, port=os.getenv('PORT', config.MS_PORT)
    )