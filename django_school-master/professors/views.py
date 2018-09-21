from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import Professor
from courses.models import Course
from sections.models import Section
# Create your views here.


def professors(request):
    professors_list = Professor.objects.order_by('-name')
    context = {
        'professors_list': professors_list,
    }
    return render(request, 'professors/index.html', context)


def detail(request, professor_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    sections = professor.section_set.all()
    return render(request, 'professors/detail.html', {'professor': professor, 'sections': sections})
    

def add_section(request, professor_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    courses_list = Course.objects.all()
    context = {
        'professor': professor,
        'courses_list': courses_list,
    }
    return render(request, 'professors/create_section.html', context)


def create_section(request, professor_id):
    course = Course.objects.get(pk=request.POST['course_id'])
    professor = Professor.objects.get(pk=professor_id)
    time = request.POST['time']
    newSection = Section(professor= professor, course= course, time = time)
    newSection.save()
    return redirect('professors:detail', professor_id=professor_id)
