from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/blog/<int:blog_id>/', views.blog_comment, name='blog_comment'),
]
