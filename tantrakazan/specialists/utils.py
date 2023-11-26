from django.core.mail import send_mail

from gallery.models import Photo
from tantrakazan.settings import DEFAULT_FROM_EMAIL
from users.models import TherapistProfile


def make_user_a_specialist(user):
    user.is_therapist = True
    user.save()
    TherapistProfile.objects.create(user=user)
    subject = 'Новый массажист ожидает подтверждения'
    count = TherapistProfile.objects.filter(is_profile_active=False).count()
    message = (f'Зарегистрирован новый массажист.'
               f' Он ожидает подтверждения своего профиля.\nВсего профилей для подтверждения: {count}')
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = ['kazan-tantra@yandex.ru']

    send_mail(subject, message, from_email, recipient_list) #TODO: Надо сделать асинхронно


def delete_specialist(user):
    user.is_therapist = False
    user.save()
    specialist_profile = TherapistProfile.objects.get(user=user)
    photos = Photo.objects.filter(user=user, is_avatar=False)
    photos.delete()
    specialist_profile.delete()
