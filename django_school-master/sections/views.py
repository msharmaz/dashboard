from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Section
# Create your views here.
def sections(request):
    return HttpResponse("sections")
def delete(request, section_id):
    section = Section.objects.get(pk=section_id)
    professor_id = section.professor.id
    section.delete()
    return redirect('professors:detail', professor_id=professor_id) 
