from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user/<int:pk>/profile/', views.user_profile, name='profile'),
    path('user/<int:pk>/profile/update/', views.profile_update, name='profile_update'),
    # path('user/<int:pk>/pwdchange/', views.pwd_change, name='pwd_change'),
    path('logout/', views.user_logout, name='logout'),
]
