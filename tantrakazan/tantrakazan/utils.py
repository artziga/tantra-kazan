import dlib
import cv2
import numpy as np
from PIL import Image

menu = [
    {'title': 'О нас', 'url_name': 'users:therapists'},
    {'title': 'Связаться', 'url_name': 'users:therapists'},
    {'title': 'Статьи', 'url_name': 'listings:listings'},
    {'title': 'Услуги', 'url_name': 'listings:listings'},
    {'title': 'Специалисты', 'url_name': 'users:therapists'},
    {'title': 'Главная', 'url_name': 'home'},
]


class DataMixin:
    @staticmethod
    def get_user_context(**kwargs):
        context = kwargs
        context['menu'] = menu
        return context


def find_face_center(photo):
    photo_data = photo.read()

    # Преобразование данных файла в массив байтов
    nparr = np.frombuffer(photo_data, np.uint8)

    # Загрузка изображения с использованием OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Инициализация детектора лиц с использованием модели HOG
    face_detector = dlib.get_frontal_face_detector()

    # Обнаружение лиц на изображении
    faces = face_detector(image, 1)
    if not faces:
        return
    if len(faces) > 1:
        return
    if len(faces) > 0:
        # Получение координат прямоугольной области первого обнаруженного лица
        face = faces[0]
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()

        # Нахождение середины лица
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        return center_x, center_y
    else:
        return None


def crop_photo(photo):
    return photo


if __name__ == '__main__':
    img = Image.open('IMG_20230702_192926.jpg')
    img.show()
    img_new = img.crop((1000, 750, 3000, 1500))
    img_new.save('IMG_20230702_192926_new.jpg', quality=95)
    img_new.show('IMG_20230702_192926_new.jpg')