from __future__ import unicode_literals
from django.contrib import admin
import models
from models import Category, Post

# Register your models here.


admin.site.register(models.Category)
admin.site.register(models.Post)

