from django.shortcuts import render, redirect
from articles.models import Section

def home(request):
    sections = Section.objects.all()
    return render(request, 'main/home.html', {'sections': sections})
