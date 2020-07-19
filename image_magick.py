import pathlib
import cv2
import numpy as np
from cv2.data import haarcascades

face_cascade_name = f'{haarcascades}/haarcascade_frontalface_alt.xml'
eyes_cascade_name = f'{haarcascades}/haarcascade_eye_tree_eyeglasses.xml'

face_cascade = cv2.CascadeClassifier()
eyes_cascade = cv2.CascadeClassifier()

face_cascade.load(cv2.samples.findFile(face_cascade_name))
eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name))


def contains_face(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.equalizeHist(img_gray)

    faces = face_cascade.detectMultiScale(img_gray)
    return any(faces)

def read_img_from_bytearray(bytearray):
    nparr = np.frombuffer(bytearray, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def save_img(path, img):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(path, img)
