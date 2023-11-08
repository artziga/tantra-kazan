from django.urls import path
from gallery import views

app_name = 'gallery'

urlpatterns = [
    path('add_photos/', views.AddPhotosView.as_view(), name='add_photos'),
    path('photo/<str:slug>/', views.PhotoDetailView.as_view(), name='photo'),
    path('photo/update/<str:slug>/', views.PhotoUpdateView.as_view(), name='update_photo_description'),
    path('photo/delete/<str:slug>', views.PhotoDeleteView.as_view(), name='delete_photo'),
]
