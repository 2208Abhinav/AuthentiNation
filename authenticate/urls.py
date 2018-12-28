from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('edit-profile', views.EditUserProfile.as_view(), name='edit_profile'),
    path('change-password', views.ChangePassword.as_view(), name='change_password'),
]
