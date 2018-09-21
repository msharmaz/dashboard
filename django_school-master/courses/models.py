from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.name

