from django.urls import path
from users import views
app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('therapist/create_profile', views.UserFormCreateView.as_view(), name='create_therapist_profile'),
    path('therapist/create_profile', views.UserFormCreateView.as_view(), name='create_therapist_profile'),
    path('therapist/create_profile', views.UserFormCreateView.as_view(), name='therapist_registration'),
    path('therapist_profile/', views.TherapistProfileDetailView.as_view(), name='my_therapist_profile'),
    path('therapist/<str:therapist>', views.TherapistProfileDetailView.as_view(), name='therapist_profile'),
    path('fill_profile/', views.AddUserAvatar.as_view(), name='add_user_avatar'),
    path('fill_therapist_profile/', views.AddTherapistAvatar.as_view(), name='add_therapist_avatar'),
    path('edit_form/', views.UserFormUpdateView.as_view(), name='edit_form'),
    path('therapists/', views.TherapistListView.as_view(), name='therapists'),
    path('form/massage_therapist/<str:username>',
         views.MassageTherapistCreateView.as_view(),
         name='massage_therapist_profile_form')
]

# from django.contrib.auth.urls




