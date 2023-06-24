from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from bleach import clean
from bleach_allowlist import markdown_tags, all_styles

markdown_attrs = {
    "*": ["id", "height", "width", "align", "border", "color", "margin", "padding"],
    "img": ["src", "alt", "title"],
    "a": ["href", "alt", "title"],
}

# Create your models here.
class Blog(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=30)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  followers = models.ManyToManyField(User, related_name="following")

  def __str__(self):
    return f"{self.title} - {self.user}"

class Post(models.Model):
  body = models.TextField()
  title = models.CharField(max_length=30)
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.title} - {self.blog}"

  @property
  def html(self):
    uncleaned_html = markdown(self.body)
    cleaned_html = clean(uncleaned_html, markdown_tags, markdown_attrs, all_styles)
    return cleaned_html

class Comment(models.Model):
  text = models.TextField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user} - {self.post} - {self.created_at}"
