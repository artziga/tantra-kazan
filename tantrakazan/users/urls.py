from django.urls import path, include
from users import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.RegisterUserCreateView.as_view(), name='registration'),
    path('login/', views.LoginUserView.as_view(), name="my_login"),
    path('auth/', include('django.contrib.auth.urls')),
    path('profile/<str:username>', views.UserProfileDetailView.as_view(), name='user'),
    path('profile/therapist/<str:username>', views.TherapistProfileDetailView.as_view(), name='therapist'),
    path('form/<str:username>', views.UserFormCreateView.as_view(), name='form'),
    path('form/massage_therapist/<str:username>',
         views.MassageTherapistCreateView.as_view(),
         name='massage_therapist_profile_form')
]
