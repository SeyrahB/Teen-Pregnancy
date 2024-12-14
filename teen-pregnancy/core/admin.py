# core/admin.py
from django.contrib import admin
from .models import Resource, ForumPost  # or any other models you want to manage via admin

# Register your models here
admin.site.register(Resource)
admin.site.register(ForumPost)
