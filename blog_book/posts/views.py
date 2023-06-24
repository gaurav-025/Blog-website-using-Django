from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from blogs.models import Post, Comment
from django import forms

class PostEditForm(forms.ModelForm):
  title = forms.CharField(max_length=40, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  body = forms.CharField(label='Body',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Post
    fields = ['title', 'body']

# Create your views here.
def post_view(request, post_id):
  post = Post.objects.get(pk=post_id)
  post_html = post.html
  return render(request, 'post_view.html', {'post': post, 'post_html': post_html})

@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('auth:login'))
def post_edit(request,post_id):
  # Check if user is the owner of the blog.
  post=Post.objects.get(id=post_id)
  # print('hi',post.blog.user,request.user,request.method);
  if(post.blog.user!=request.user):
    messages.add_message(request, messages.ERROR, "You do not have the permission to edit this blog.")
    return redirect('posts:post_view',post_id=post_id)
  
  if request.method == 'POST':
    form = PostEditForm(request.POST,initial={'title': 'Aakanksha'})
    if form.is_valid():
      post_data = form.save(commit=False)
      try:
        post.title = post_data.title
        post.body = post_data.body
        # print(post_data)
        post.save()
        messages.add_message(request, messages.SUCCESS, "Your post was successfully edited.")
      except:
        messages.add_message(request, messages.ERROR, "An error occurred while editing the post.")
        return render(request, 'post_edit.html', {'form': form, 'post': post})
      return redirect('posts:post_view',post_id=post_id)
    return render(request, 'post_edit.html', {'form': form, 'post': post})
  else:
    form = PostEditForm({'title': post.title, 'body': post.body})
    return render(request, 'post_edit.html', {'form': form, 'post': post})

@require_POST
@login_required(login_url=reverse_lazy('auth:login'))
def comment_create(request, post_id):
  text = request.POST.get('text')
  comment = Comment.objects.create(post_id=post_id, text=text, user=request.user)
  comment.save()
  messages.add_message(request, messages.SUCCESS, "Comment created.")
  return redirect('posts:post_view', post_id=post_id)

@require_http_methods(['DELETE'])
@login_required(login_url=reverse_lazy('auth:login'))
def comment_delete(request, post_id, comment_id):
  comment = Comment.objects.get(id=comment_id)
  if request.method == 'DELETE':
    if request.user.id == comment.user.id:
      comment.delete()
      messages.add_message(request, messages.SUCCESS, "Comment deleted.")
    else:
      messages.add_message(request, messages.ERROR, "You cannot delete this comment.")
    return redirect('posts:post_view', post_id=post_id)