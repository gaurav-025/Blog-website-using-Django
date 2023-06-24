from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from blogs.models import Blog, Post
from django import forms

class BlogCreationForm(forms.ModelForm):
  title = forms.CharField(max_length=30, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  description = forms.CharField(max_length=500, label='Description',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Blog
    fields = ['title', 'description']

class BlogEditForm(forms.ModelForm):
  title = forms.CharField(max_length=40, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  description = forms.CharField(max_length=500, label='Description',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Blog
    fields = ['title', 'description']

class PostCreationForm(forms.ModelForm):
  title = forms.CharField(max_length=40, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  body = forms.CharField(label='Body',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Post
    fields = ['title', 'body']

# Create your views here.
@require_GET
def index(request):
  blogs = Blog.objects.all()
  return render(request, 'index.html', {'blogs': blogs})

@require_GET
def blog_view(request, blog_id):
  blog = Blog.objects.get(pk=blog_id)
  posts = blog.posts.all()
  following = False
  if request.user.is_authenticated:
    following = request.user.following.filter(pk=blog_id).exists()
  return render(request, 'blog_view.html', {'blog': blog, 'posts': posts, 'following': following})

@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('auth:login'))
def blog_create(request):
  if request.method == 'POST':
    form = BlogCreationForm(request.POST)
    # print(form)
    if form.is_valid():
      blog = form.save(commit=False)
      blog.user = request.user
      blog.save()
      messages.add_message(request, messages.SUCCESS, "Your blog was created successfully")
      return redirect('blogs:blog_view', blog_id=blog.id)
    return render(request, 'blog_create.html', {'form': form})
  else:
    form = BlogCreationForm()
    return render(request, 'blog_create.html', {'form': form})

@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('auth:login'))
def blog_edit(request,blog_id):
  # Check if user is the owner of the blog.
  blog=Blog.objects.get(id=blog_id)
  if(blog.user!=request.user):
    messages.add_message(request, messages.ERROR, "You do not have the permission to edit this blog.")
    return redirect('blogs:blog_view',blog_id=blog_id)
  
  if request.method == 'POST':
    form = BlogEditForm(request.POST,initial={'title': 'Aakanksha'})
    if form.is_valid():
      blog_data = form.save(commit=False)
      try:
        blog.title = blog_data.title
        blog.description = blog_data.description
        blog.save()
        messages.add_message(request, messages.SUCCESS, "Your blog was successfully edited.")
      except:
        return render(request, 'blog_edit.html', {'form': form})
      return redirect('blogs:blog_view',blog_id=blog_id)
    return render(request, 'blog_edit.html', {'form': form, 'blog': blog})
  else:
    form = BlogEditForm()
    return render(request, 'blog_edit.html', {'form': form, 'blog': blog})

@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('auth:login'))
def post_create(request, blog_id):
  blog=Blog.objects.get(id=blog_id)
  if(blog.user!=request.user):
    messages.add_message(request, messages.ERROR, "You do not have the permission to create post on this blog.")
    return redirect('blogs:blog_view',blog_id=blog_id)

  if request.method == 'POST':
    form = PostCreationForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.blog = blog
      post.save()
      messages.add_message(request, messages.SUCCESS, "Your post was successfully created.")
      return redirect('posts:post_view', post_id=post.id)
    return render(request, 'post_create.html', {'form': form, 'blog': blog})
  else:
    form = PostCreationForm()
    return render(request, 'post_create.html', {'form': form, 'blog': blog})

@require_http_methods(['DELETE', 'POST'])
@login_required(login_url=reverse_lazy('auth:login'))
def blog_follower(request, blog_id):
  if request.method == 'POST':
    if not request.user.following.filter(pk=blog_id).exists():
      request.user.following.add(blog_id)
  elif request.method == 'DELETE':
    if request.user.following.filter(pk=blog_id).exists():
      request.user.following.remove(blog_id)
  return redirect('blogs:blog_view', blog_id=blog_id)