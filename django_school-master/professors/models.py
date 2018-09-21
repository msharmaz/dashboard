from django.db import models

# Create your models here.


class Professor(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.name

