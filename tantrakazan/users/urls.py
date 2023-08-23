from django.urls import path
from users import views
app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('therapist_profile/', views.TherapistProfileDetailView.as_view(), name='therapist_profile'),
    path('profile_completion/', views.UserProfileCompletionView.as_view(), name='profile_completion'),
    path(
        'profile_completion/therapist/',
        views.TherapistProfileCompletionView.as_view(),
        name='therapist_profile_completion'),
    path('therapist/<str:therapist>/', views.TherapistProfileDetailView.as_view(), name='therapist_profile'),
    path('fill_profile/', views.AddUserAvatar.as_view(), name='add_user_avatar'),
    path('fill_therapist_profile/', views.AddTherapistAvatar.as_view(), name='add_therapist_avatar'),
    path('edit_profile/', views.UserFormUpdateView.as_view(), name='edit_profile'),
    path('therapists/', views.TherapistListView.as_view(), name='therapists'),
    path('therapists/on_map', views.TherapistOnMapListView.as_view(), name='therapists_on_map'),
]

# from django.contrib.auth.urls




