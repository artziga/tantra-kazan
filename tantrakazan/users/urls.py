from django.urls import path

from tantrakazan.utils import AddressAutocomplete
from users import views
app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('become_a_specialist/', views.become_a_specialist, name='become_a_specialist'),
    path('become_a_specialist/confirm/', views.become_a_specialist_confirmation,
         name='become_a_specialist_confirmation'),
    path('delete_a_specialist/', views.become_a_specialist, name='delete_a_specialist'),
    path('delete_a_specialist/confirm/', views.become_a_specialist_confirmation,
         name='delete_a_specialist_confirmation'),
    path('specialist/<str:specialist_username>/', views.SpecialistProfileDetailView.as_view(), name='specialist_profile'),
    path('avatar/', views.AddAvatar.as_view(), name='add_avatar'),
    path('edit_profile/', views.SpecialistProfileWizard.as_view(), name='edit_profile'),
    path('therapists/', views.SpecialistsListView.as_view(), name='specialists'),
    path('therapists/on_map', views.TherapistOnMapListView.as_view(), name='specialists_on_map'),
]





