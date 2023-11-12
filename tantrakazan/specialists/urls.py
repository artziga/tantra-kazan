from django.urls import path

from specialists import views
app_name = 'specialists'
urlpatterns = [
    path('', views.SpecialistsListView.as_view(), name='specialists'),
    path('profile/', views.SpecialistProfileDetailView.as_view(), name='profile'),
    path('become_a_specialist/', views.become_a_specialist, name='become_a_specialist'),
    path('become_a_specialist/confirm/', views.become_a_specialist_confirmation,
         name='become_a_specialist_confirmation'),
    path('delete_a_specialist/', views.become_a_specialist, name='delete_a_specialist'),
    path('delete_a_specialist/confirm/', views.become_a_specialist_confirmation,
         name='delete_a_specialist_confirmation'),
    path('specialist/<str:specialist_username>/', views.SpecialistProfileDetailView.as_view(), name='specialist_profile'),
    path('edit_profile/', views.SpecialistProfileWizard.as_view(), name='edit_profile'),
    ]






