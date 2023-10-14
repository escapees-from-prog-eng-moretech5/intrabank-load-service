from flask import Flask, jsonify
import requests
import json
import os
import people_detection
import time
from datetime import datetime, timezone


app = Flask(__name__)

URL = "https://example.com/api"
JSON_FILE = "response.json"
PASSWORD = 'jAAGQtsCBsByGFYkzHmH'
protopath = "NN\MobileNetSSD_deploy.prototxt"
modelpath = "NN\MobileNetSSD_deploy.caffemodel"
BACKEND_URL = 'URL'


def get_response_and_save():
    response = requests.get(URL)
    with open(JSON_FILE, 'w') as f:
        json.dump(response.json(), f)


def provide_saved_response():
    with open(JSON_FILE, 'r') as f:
        return json.load(f)


def neural_network_response(ip):
    cam = people_detection.Camera(ip, protopath=protopath, modelpath=modelpath)
    cam.start_camera_for_duration(0.2)
    cam.start_camera()


@app.route('/api/v1/place/register', methods=['POST'])
def fetch_data():
    if not os.path.exists(JSON_FILE):
        get_response_and_save()
        return jsonify({"message": "Запрос отправлен и ответ сохранен в JSON-файл."})
    else:
        return jsonify({"message": "Данные уже сохранены."})


@app.route('/api/v1/place', methods=['POST'])
def send_data():
    if not os.path.exists(JSON_FILE):
        return jsonify({"message": "JSON-файл не найден. Сначала получите данные."})
    else:
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
            user_id = data["id"]
            ips = [camera["CameraIp"] for camera in data["cameras"]]
            results = {ip: neural_network_response(ip) for ip in ips}
            for i in range(len(results.keys())):
                response = {"id": user_id,
                            "officeId": data["cameras"]["officeId"][i],
                            "current": int(results[data["cameras"]["cameraId"][i]]),
                            "time": datetime.now(timezone.utc).isoformat()}
                requests.post(BACKEND_URL, json=response)
        return jsonify({"message": "Данные успешно отправлены."})


if __name__ == "__main__":
    app.run(debug=True)
