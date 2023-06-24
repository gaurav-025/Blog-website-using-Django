from django.urls import path
from .views import * 

app_name="blogs"

urlpatterns = [
  path('', index, name='index'),
  path('<int:blog_id>/', blog_view, name='blog_view'),
  path('new/', blog_create, name='blog_create'),
  path('<int:blog_id>/edit/',blog_edit,name='blog_edit'),
  path('<int:blog_id>/posts/new/', post_create, name='post_create'),
  path('<int:blog_id>/followers/', blog_follower, name='blog_follower')
]