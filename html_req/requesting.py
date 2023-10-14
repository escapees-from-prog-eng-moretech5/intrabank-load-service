import requests
import json
import os
import people_detection
from datetime import datetime, timezone
from flask import Flask, jsonify
import time


protopath = "NN\MobileNetSSD_deploy.prototxt"
modelpath = "NN\MobileNetSSD_deploy.caffemodel"


def neural_network_response(ip):
    cam = people_detection.Camera(ip, protopath=protopath, modelpath=modelpath)
    cam.start_camera_for_duration(0.2)
    cam.start_camera()


def save_response_to_json(url, file_name):
    if not os.path.exists(file_name):
        response = requests.post(url)

        if response.status_code == 200:
            data = response.json()
            with open(file_name, 'w') as json_file:
                json.dump(data, json_file)
            print(f"Данные сохранены в {file_name}")
        else:
            print(f"Ошибка при запросе: {response.status_code}")
    else:
        print(f"Файл {file_name} уже существует. Запрос не выполнен.")


def send_post_request(url, json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        user_id = data["id"]
        ips = [camera["CameraIp"] for camera in data["cameras"]]
        results = {ip: neural_network_response(ip) for ip in ips}
        for i in range(len(results.keys())):
            response = {"id": user_id,
                        "officeId": data["cameras"]["officeId"][i],
                        "current": int(results[data["cameras"]["cameraId"][i]]),
                        "time": datetime.now(timezone.utc).isoformat()}
            requests.post(url, json=response)

    return jsonify({"message": "Данные успешно отправлены."})


def periodic_requests():
    while True:
        save_response_to_json('/api/v1/place/register', 'response_data.json')
        send_post_request('/api/v1/place', 'response_data.json')
        time.sleep(1800)
