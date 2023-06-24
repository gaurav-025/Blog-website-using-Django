from django.contrib import admin
from .models import Blog, Post, Comment

# Register your models here.
@admin.register(Blog, Post, Comment)
class Admin(admin.ModelAdmin):
  pass