from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Course
# Create your views here.


def courses(request):
    courses_list = Course.objects.order_by('-name')
    context = {
        'courses_list': courses_list,
    }
    return render(request, 'courses/index.html', context)


def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    sections = course.section_set.all()
    context = {
        'course': course,
        'sections': sections,
    } 
    return render(request, 'courses/detail.html', context)
    


