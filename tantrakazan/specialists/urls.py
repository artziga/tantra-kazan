from django.urls import path

from specialists import views
app_name = 'specialists'
urlpatterns = [
    path('', views.SpecialistsListView.as_view(), name='specialists'),

    path('profile/', views.SpecialistSelfProfileDetailView.as_view(), name='profile'),
    path('become_a_specialist/', views.become_a_specialist, name='become_a_specialist'),
    path('become_a_specialist/confirm/', views.become_a_specialist_confirmation,
         name='become_a_specialist_confirmation'),
    path('delete_a_specialist/', views.become_a_specialist, name='delete_a_specialist'),
    path('delete_a_specialist/confirm/', views.become_a_specialist_confirmation,
         name='delete_a_specialist_confirmation'),
    path('edit_profile/<int:pk>', views.SpecialistProfileWizard.as_view(), name='edit_profile'),
    path(
        "password_change/", views.UserPasswordChangeView.as_view(), name="change_password"
    ),
    path('get_social_info/', views.get_social_info, name='get_social_info'),
    path('<str:specialist_username>/', views.SpecialistProfileDetailView.as_view(), name='specialist_profile'),

    ]






