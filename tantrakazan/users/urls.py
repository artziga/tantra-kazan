from django.urls import path, include
from users import views
app_name = 'users'

urlpatterns = [
    path('registration/', views.RegisterUserCreateView.as_view(), name='registration'),
    path('registration/done', views.RegisterDone.as_view(), name='registration_done'),
    path('registration/activate/<str:sign>/ ', views.user_activate, name='register_activate'),
    path('change_password/', views.UserPasswordChangeView.as_view(), name='change_password'),
    path('therapist_registration/', views.RegisterTherapistCreateView.as_view(), name='therapist_registration'),
    path('login/', views.LoginUserView.as_view(), name="my_login"),
    path('auth/', include('django.contrib.auth.urls')),
    path('profile/', views.ProfileView.as_view(), name='my_profile'),
    path('therapist_profile/', views.TherapistProfileDetailView.as_view(), name='my_therapist_profile'),
    path('therapist/<str:therapist>', views.TherapistProfileDetailView.as_view(), name='therapist_profile'),
    path('fill_profile/', views.AddUserAvatar.as_view(), name='add_user_avatar'),
    path('fill_therapist_profile/', views.AddTherapistAvatar.as_view(), name='add_therapist_avatar'),
    path('therapist/create_profile', views.UserFormCreateView.as_view(), name='create_therapist_profile'),
    path('edit_form/', views.UserFormUpdateView.as_view(), name='edit_form'),
    path('therapists/', views.TherapistListView.as_view(), name='therapists'),
    path('form/massage_therapist/<str:username>',
         views.MassageTherapistCreateView.as_view(),
         name='massage_therapist_profile_form')
]






