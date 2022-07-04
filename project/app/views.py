from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from app.decorators import admin_required
from .models import Course, MyUser, Role
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, MyUserEditForm, StudentForm, ProfessorForm

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
            return HttpResponse("Submit Failure! Invalid Form!")

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
            return HttpResponse("Submit Failure! Invalid Form!")

@admin_required
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete() 
    return redirect('all_courses')

@admin_required
def all_students(request):
    students = MyUser.objects.filter(role_id__role=Role.STUDENT)
    return render(request, 'all_students.html', {"students": students})

@admin_required
def all_professors(request):
    professors = MyUser.objects.filter(role_id__role=Role.PROFESOR)
    return render(request, 'all_professors.html', {"professors": professors})

@admin_required
def add_user(request, role):
    if request.method == 'GET':
        if role == Role.STUDENT:
            userForm = StudentForm()
        elif role == Role.PROFESOR:
            userForm = ProfessorForm()
        return render(request, 'add_user.html', {'form': userForm})
    elif request.method == 'POST':
        if role == Role.STUDENT:
            userForm = StudentForm(request.POST)
            if userForm.is_valid():
                userForm.save()
                return redirect('all_students')
            else:
                return HttpResponse("Submit Failure! Invalid Form!")
        elif role == Role.PROFESOR:
            userForm = ProfessorForm(request.POST)
            if userForm.is_valid():
                userForm.save()
                return redirect('all_professors')
            else:
                return HttpResponse("Submit Failure! Invalid Form!")

@admin_required
def edit_user(request, user_id):           
    user = MyUser.objects.get(id=user_id)
    if request.method == 'GET':
        userForm = MyUserEditForm(instance=user)
        return render(request, 'edit_user.html', {'form': userForm})
    elif request.method == 'POST':
        userForm = MyUserEditForm(request.POST, instance=user)
        if userForm.is_valid():
            userForm.save()
            return redirect('all_courses')
        else:
            return HttpResponse("Submit Failure! Invalid Form!")

@admin_required
def delete_user(request, user_id):
    user = MyUser.objects.get(id=user_id)
    user.delete() 
    return redirect('all_courses')

@admin_required
def students_ft(request):
    students = MyUser.objects.filter(role_id__role=Role.STUDENT, status="redovni")
    return render(request, 'all_students.html', {'students': students})

@admin_required
def students_pt(request):
    students = MyUser.objects.filter(role_id__role=Role.STUDENT, status="izvanredni")
    return render(request, 'all_students.html', {'students': students})