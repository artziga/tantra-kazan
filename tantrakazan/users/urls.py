from django.urls import path

from tantrakazan.utils import AddressAutocomplete
from users import views
app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('become_a_therapist/', views.become_a_therapist, name='become_a_therapist'),
    path('become_a_therapist/confirm/', views.become_a_therapist_confirmation,
         name='become_a_therapist_confirmation'),
    path('delete_a_therapist/', views.become_a_therapist, name='delete_a_therapist'),
    path('delete_a_therapist/confirm/', views.become_a_therapist_confirmation,
         name='delete_a_therapist_confirmation'),
    path('therapist/<str:therapist_username>/', views.TherapistProfileDetailView.as_view(), name='specialist_profile'),
    path('avatar/', views.AddAvatar.as_view(), name='add_avatar'),
    path('edit_profile/', views.TherapistProfileWizard.as_view(), name='edit_profile'),
    path('therapists/', views.SpecialistsListView.as_view(), name='therapists'),
    path('therapists/on_map', views.TherapistOnMapListView.as_view(), name='therapists_on_map'),
]





