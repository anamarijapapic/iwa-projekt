from django.shortcuts import render
from .models import Course
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'all_courses.html', {"courses": courses})