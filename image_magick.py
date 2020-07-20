import pathlib
import cv2
import numpy as np
from cv2.data import haarcascades

face_cascade_name = f'{haarcascades}/haarcascade_frontalface_alt.xml'

face_cascade = cv2.CascadeClassifier()

face_cascade.load(cv2.samples.findFile(face_cascade_name))


def contains_face(img: np.ndarray) -> bool:
    """
    Face detection using Haar cascade
    :param img: image to process
    :return: True if at least one face detected
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.equalizeHist(img_gray)

    faces = face_cascade.detectMultiScale(img_gray)
    return len(faces) > 0


def read_img_from_bytearray(bytestr) -> np.ndarray:
    """
    Reads image from binary data
    :param bytestr: binary data
    :return: image
    """
    nparr = np.frombuffer(bytestr, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


def save_img(path: str, img: np.ndarray):
    """
    Saves image to path
    :param path:
    :param img:
    :return:
    """
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), img)
