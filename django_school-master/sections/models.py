from django.db import models

# Create your models here.
class Section(models.Model):
    professor = models.ForeignKey('professors.Professor', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    time = models.TimeField()
    def __str__(self):
        return self.course.name + " taught by  " + self.professor.name + " @ " + self.time.__str__()
