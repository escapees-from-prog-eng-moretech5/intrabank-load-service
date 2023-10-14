import cv2
import datetime
import imutils
import numpy as np
import requests
import time


class Person:
    def __init__(self, person_id, box):
        self.person_id = person_id
        self.box = box
        self.frames_counter = 0


class Camera:
    def __init__(self, video_path, protopath, modelpath):
        self.cap = cv2.VideoCapture(video_path)
        self.detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.active_people = []
        self.next_person_id = 1

        self.use_camera = False
        self.cap = cv2.VideoCapture(video_path) if not self.use_camera else cv2.VideoCapture(0)

    def start_camera(self):
        self.use_camera = True
        self.cap = cv2.VideoCapture(0)

    def stop_camera(self):
        self.use_camera = False
        self.cap.release()
        cv2.destroyAllWindows()

    def _get_person_id(self, box):
        threshold = 50
        for person in self.active_people:
            (startX_prev, startY_prev, endX_prev, endY_prev) = person.box
            (startX, startY, endX, endY) = box
            if abs(startX - startX_prev) < threshold and abs(startY - startY_prev) < threshold:
                person.frames_counter = 0
                person.box = box
                return person.person_id

        new_person = Person(self.next_person_id, box)
        self.active_people.append(new_person)
        self.next_person_id += 1
        return new_person.person_id

    def start_camera_for_duration(self, duration):
        fps_start_time = datetime.datetime.now()
        total_frames = 0
        start_time = time.time()

        while time.time() - start_time < duration:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = imutils.resize(frame, width=600)
            total_frames += 1

            (H, W) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            self.detector.setInput(blob)
            detections = self.detector.forward()
            self._draw_boxes(frame, detections, H, W)

            fps_end_time = datetime.datetime.now()
            time_diff = fps_end_time - fps_start_time
            fps = total_frames / (time_diff.seconds if time_diff.seconds != 0 else 1)
            fps_text = "FPS: {:.2f}".format(fps)
            cv2.putText(frame, fps_text, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)

            #cv2.imshow("Application", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

            self.active_people = [person for person in self.active_people if person.frames_counter < 10]
            for person in self.active_people:
                person.frames_counter += 1

        self.cap.release()
        cv2.destroyAllWindows()

        print(f"Max Person ID: {self.next_person_id - 1}")
        return self.next_person_id - 1

    def _draw_boxes(self, frame, detections, H, W):
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] != "person":
                    continue

                person_box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = person_box.astype("int")

                person_id = self._get_person_id((startX, startY, endX, endY))
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, f"ID: {person_id}", (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


if __name__ == "__main__":
    protopath = "NN\MobileNetSSD_deploy.prototxt"
    modelpath = "NN\MobileNetSSD_deploy.caffemodel"
    video_path = 'vids_tests/pexels_videos_1338598 (1080p).mp4'
    #video_path = 'vids_tests/production_id_3687560 (2160p).mp4'
    #video_path = 'vids_tests/production_id_4174175 (1080p).mp4'
    cam = Camera(video_path, protopath, modelpath)
    cam.start_camera_for_duration(0.2)
    cam.start_camera()

