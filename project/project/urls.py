"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('edit_course/<int:course_id>/', views.edit_course, name="edit_course"),
    path('delete_course/<int:course_id>/', views.delete_course, name="delete_course"),
    path('all_students/', views.all_students, name='all_students'),
    path('all_professors/', views.all_professors, name='all_professors'),
    path('add_user/<str:role>/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name="edit_user"),
    path('delete_user/<int:user_id>/', views.delete_user, name="delete_user"),
    path('students_ft/', views.students_ft, name="students_ft"),
    path('students_pt/', views.students_pt, name="students_pt"),
    path('students_final_year/', views.students_final_year, name='students_final_year'),
    path('enrollment_list/<int:student_id>/', views.enrollment_list, name='enrollment_list'),
    path('enroll_course/<int:student_id>/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('disenroll_course/<int:student_id>/<int:course_id>/', views.disenroll_course, name='disenroll_course'),
    path('students_on_course/<int:course_id>/', views.students_on_course, name="students_on_course"),
    path('students_on_course/<int:course_id>/<str:status>/', views.students_on_course_filter, name='students_on_course_filter'),
    path('change_course_status/<int:record_id>/', views.change_course_status, name="change_course_status"),
]