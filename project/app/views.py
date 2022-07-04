from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed

from app.decorators import admin_required
from .models import Course
from django.contrib.auth.decorators import login_required
from .forms import CourseForm

# Create your views here.

@login_required
def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'all_courses.html', {"courses": courses})

@admin_required
def add_course(request):
    if request.method == 'GET':
        courseForm = CourseForm()
        return render(request, 'add_course.html', {'form': courseForm})
    elif request.method == 'POST':
        courseForm = CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
            return redirect('all_courses')
    else:
        return HttpResponseNotAllowed()

@admin_required
def edit_course(request, course_id):           
    course = Course.objects.get(id=course_id)
    if request.method == 'GET':
        courseForm = CourseForm(instance=course)
        return render(request, 'edit_course.html', {'form': courseForm})
    elif request.method == 'POST':
        courseForm = CourseForm(request.POST, instance=course)
        if courseForm.is_valid():
            courseForm.save()
            return redirect('all_courses')
    else:
        return HttpResponseNotAllowed()

@admin_required
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete() 
    return redirect('all_courses')