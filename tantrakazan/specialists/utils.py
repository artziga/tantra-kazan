from users.models import TherapistProfile


def make_user_a_specialist(user):
    user.is_therapist = True
    user.save()
    TherapistProfile.objects.create(user=user)