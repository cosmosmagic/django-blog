from django.urls import path, include
from .views import IndexView, ArchiveView, BlogDetailView, CategoryView, TagView

app_name = 'myblog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('archives/<int:year>/<int:month>/', ArchiveView.as_view(), name='archives'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag'),
]
