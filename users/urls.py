from django.urls import path
from . import views


app_name='users'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login',
    path('user/(?P<int:pk>\d+/profile/',views.profile,name='profile'),
    path('user/?P<int:pk>\d+/profile/update/',views.profile_update,name='profile_update),
    path('user/?P<int:pk>\d+/pwdchange/',views.pwd_change,name='pwd_change'),
    path('logout/',views.logout,name='logout'),
    ]
