from django.contrib import admin

# Register your models here.

import models

from models import Comment, Message, User

# Register your models here.


admin.site.register(models.User)
admin.site.register(models.Comment)
admin.site.register(models.Message)
