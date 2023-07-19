import dlib
import cv2
import numpy as np
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from collections import namedtuple

Borders = namedtuple('Borders', 'left top right bottom')


def prepare_image(img):
    if isinstance(img, InMemoryUploadedFile):
        img_data = img.read()
        nparr = np.frombuffer(img_data, np.uint8)
        cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return cv2_image


def find_face(img):
    cv2_image = prepare_image(img=img)
    # Инициализация детектора лиц с использованием модели HOG
    face_detector = dlib.get_frontal_face_detector()

    # Обнаружение лиц на изображении
    faces = face_detector(cv2_image, 1)
    if not faces:
        return
    if len(faces) > 1:
        return
    else:
        # Получение координат прямоугольной области первого обнаруженного лица
        face = faces[0]
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()

        return left, top, right, bottom


def get_frames(image_size: tuple, face_borders: Borders = None, margin_percent: float = 0.5) -> Borders:
    image_width, image_high = image_size
    if face_borders is None:
        if image_width == image_high:
            return Borders(left=0, right=image_width, top=0, bottom=image_high)
        if image_width < image_high:
            dif = image_high - image_width
            left = 0
            right = image_width
            top = dif / 2
            bottom = image_high - dif / 2
        else:
            dif = image_width - image_high
            top = 0
            bottom = image_high
            left = dif / 2
            right = image_width - dif / 2
        return Borders()

    face_high = face_borders.bottom - face_borders.top
    face_width = face_borders.right - face_borders.left
    face_size = face_width if face_width >= face_high else face_high
    margin = face_size * margin_percent

    left = face_borders.left - margin if face_borders.left - margin >= 0 else 0
    right = face_borders.right + margin if face_borders.right + margin <= image_width else image_width
    top = face_borders.top - margin if face_borders.top - margin >= 0 else 0
    bottom = face_borders.bottom + margin if face_borders.bottom + margin <= image_high else image_high

    margin = min(face_borders.left - left,
                 right - face_borders.right,
                 face_borders.top - top,
                 bottom - face_borders.bottom)

    left = face_borders.left - margin
    right = face_borders.right + margin
    top = face_borders.top - margin
    bottom = face_borders.bottom + margin

    return Borders(left=left, top=top, right=right, bottom=bottom)


def get_image_to_upload(image):
    buffer = BytesIO()
    # Сохранение изображения в буфере
    image.save(buffer, format='JPEG')
    image_to_upload = InMemoryUploadedFile(
        buffer,
        'avatar',
        'image/jpeg',
        buffer.tell(),
        None,
        None
    )
    return image_to_upload


def convert_to_image(inmemory_uploaded_file):
    # Создание буфера в памяти
    buffer = BytesIO()

    # Запись данных из InMemoryUploadedFile в буфер
    for chunk in inmemory_uploaded_file.chunks():
        buffer.write(chunk)
    buffer.seek(0)

    # Создание объекта Image из буфера
    image = Image.open(buffer)

    return image


def crop_face(uploaded_image):
    fb = find_face(uploaded_image)
    if fb:
        left, top, right, bottom = fb
        face_borders = Borders(left=left, top=top, right=right, bottom=bottom)
    else:
        face_borders = None
    image_file = convert_to_image(uploaded_image)
    size = image_file.size
    avatar_borders = get_frames(image_size=size, face_borders=face_borders)
    cropped_image = image_file.crop(avatar_borders)
    return get_image_to_upload(cropped_image)


if __name__ == '__main__':
    img = Image.open('IMG_20230702_192926.jpg')
    # find_face(img)
