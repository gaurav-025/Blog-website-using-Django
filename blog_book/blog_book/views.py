from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from blogs.models import Blog, Post

# Create your views here.

def home_view(request):
  return render(request, "home.html")

@login_required(login_url=reverse_lazy('auth:login'))
def feed_view(request):
  posts = Post.objects.filter(blog__pk__in=request.user.following.all()).order_by('created_at')
  return render(request, "feed.html", {"posts": posts})