from django.urls import path

from tantrakazan.utils import AddressAutocomplete
from users import views
app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('avatar/', views.AddAvatar.as_view(), name='add_avatar'),
    path('favorite/', views.Favorite.as_view(), name='favorite'),
    path('edit_profile/<int:pk>', views.EditProfile.as_view(), name='edit_profile')
]





