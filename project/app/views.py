from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.decorators import admin_required
from .models import Course, EnrollmentList, MyUser, Role
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, MyUserEditForm, StudentForm, ProfessorForm, CourseStatusForm
from django.db.models import Q
from django.db.models import Count, Sum

# Create your views here.

@login_required
def home(request):
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.PROFESSOR:
        return redirect('all_courses')
    return redirect('enrollment_list', request.user.id)

@login_required
def all_courses(request):
    # get course stats to show message in template "x students passed the course (y full-time students and z part-time students)"
    if request.user.role.role == Role.ADMIN:
        # courses = Course.objects.all()
        courses = Course.objects.annotate(
            num_students_passed=Count('enrollmentlist', filter=Q(enrollmentlist__status='polozen')), 
            num_ft_passed=Count('enrollmentlist', filter=Q(enrollmentlist__status='polozen') & Q(enrollmentlist__student__status='redovni')),
            num_pt_passed=Count('enrollmentlist', filter=Q(enrollmentlist__status='polozen') & Q(enrollmentlist__student__status='izvanredni'))
        )
    elif request.user.role.role == Role.PROFESSOR:
        # courses = Course.objects.filter(lecturer=request.user.id)
        courses = Course.objects.filter(lecturer=request.user.id).annotate(
            num_students_passed=Count('enrollmentlist', filter=Q(enrollmentlist__status='polozen')), 
            num_ft_passed=Count('enrollmentlist', filter=Q(enrollmentlist__status='polozen') & Q(enrollmentlist__student__status='redovni')),
            num_pt_passed=Count('enrollmentlist', filter=Q(enrollmentlist__status='polozen') & Q(enrollmentlist__student__status='izvanredni'))
        )
    else:
        return HttpResponse("Access Forbidden!")
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
    students = MyUser.objects.filter(role_id__role=Role.STUDENT).order_by('last_name', 'first_name')
    return render(request, 'all_students.html', {"students": students})

@admin_required
def all_professors(request):
    professors = MyUser.objects.filter(role_id__role=Role.PROFESSOR).order_by('last_name', 'first_name')
    return render(request, 'all_professors.html', {"professors": professors})

@admin_required
def add_user(request, role):
    if request.method == 'GET':
        if role == Role.STUDENT:
            userForm = StudentForm()
        elif role == Role.PROFESSOR:
            userForm = ProfessorForm()
        return render(request, 'add_user.html', {'form': userForm, 'role': role.capitalize()})
    elif request.method == 'POST':
        if role == Role.STUDENT:
            userForm = StudentForm(request.POST)
            if userForm.is_valid():
                userForm.save()
                return redirect('all_students')
            else:
                return HttpResponse("Submit Failure! Invalid Form!")
        elif role == Role.PROFESSOR:
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
            if user.role.role == Role.STUDENT:
                return redirect('all_students')
            else:
                return redirect('all_professors')
        else:
            return HttpResponse("Submit Failure! Invalid Form!")

@admin_required
def delete_user(request, user_id):
    user = MyUser.objects.get(id=user_id)
    user.delete() 
    if user.role.role == Role.STUDENT:
        return redirect('all_students')
    return redirect('all_professors')

@admin_required
def students_ft(request):
    # full-time students
    students = MyUser.objects.filter(role_id__role=Role.STUDENT, status="redovni").order_by('last_name', 'first_name')
    return render(request, 'all_students.html', {'students': students})

@admin_required
def students_pt(request):
    # part-time students
    students = MyUser.objects.filter(role_id__role=Role.STUDENT, status="izvanredni").order_by('last_name', 'first_name')
    return render(request, 'all_students.html', {'students': students})

@admin_required
def students_last_year(request):
    # last year students
    last_year_students = []
    students = MyUser.objects.filter(role_id__role=Role.STUDENT)
    for student in students:
        records = EnrollmentList.objects.filter(student=student)
        still_first_year = False
        for record in records:
            if (((record.course.semester_ft == 1 or record.course.semester_ft == 2) and student.status == 'redovni') or ((record.course.semester_pt == 1 or record.course.semester_pt == 2) and student.status == 'izvanredni')) and record.status != 'polozen':
                # check if there is any 1st year courses that student didn't pass
                still_first_year = True
                break
            if (((record.course.semester_ft == 5 or record.course.semester_ft == 6) and student.status == 'redovni') or ((record.course.semester_pt == 7 or record.course.semester_pt == 8) and student.status == 'izvanredni')) and student not in last_year_students:
                last_year_students.append(student)
        if still_first_year and student in last_year_students:
            last_year_students.remove(student)
    return render(request, 'all_students.html', {'students': last_year_students})

@login_required
def enrollment_list(request, student_id):
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.STUDENT and request.user.id == student_id:
        try:
            student = MyUser.objects.get(id=student_id)
        except MyUser.DoesNotExist:
            student = None
            return HttpResponse("Access Denied! User does not exist!")
        if student.role.role != Role.STUDENT:
            return HttpResponse("Access Denied! User is not student!")

        # block enroll for 3rd/4rd year courses if not all courses from 1st year are passed
        if student.status == 'redovni':
            higher_year_courses_ids = Course.objects.filter(Q(semester_ft=5) | Q(semester_ft=6)).values_list('id', flat=True)
            first_year_courses_left = EnrollmentList.objects.filter(Q(student=student) & Q(Q(course__semester_ft=1) | Q(course__semester_ft=2)) & ~Q(status='polozen'))
        else:
            higher_year_courses_ids = Course.objects.filter(Q(semester_pt=5) | Q(semester_pt=6) | Q(semester_pt=7) | Q(semester_pt=8)).values_list('id', flat=True)
            first_year_courses_left = EnrollmentList.objects.filter(Q(student=student) & Q(Q(course__semester_pt=1) | Q(course__semester_pt=2)) & ~Q(status='polozen'))
        if first_year_courses_left:
            block_enroll_courses = Course.objects.exclude(~Q(id__in=higher_year_courses_ids)).order_by('id')
        else:
            block_enroll_courses = []

        enrollment_record_course_ids = EnrollmentList.objects.filter(student=student).values_list('course_id', flat=True)
        available_courses = Course.objects.exclude(id__in=enrollment_record_course_ids)

        # block disenroll if course is passed/lost signature    
        enrollment_record_block_disenroll_ids = EnrollmentList.objects.filter(Q(status="polozen") | Q(status="izgubljen_potpis"), student=student).values_list('course_id', flat=True)
        block_disenroll_courses = Course.objects.exclude(~Q(id__in=enrollment_record_block_disenroll_ids)).order_by('id')
        
        if student.status == 'redovni':
            enrolled_courses = Course.objects.exclude(~Q(id__in=enrollment_record_course_ids)).order_by('id')
        else:
            enrolled_courses = Course.objects.exclude(~Q(id__in=enrollment_record_course_ids)).order_by('semester_pt', 'id')

        # ECTS calculation (total, passed, left)
        total_ects = EnrollmentList.objects.filter(student=student).aggregate(total_ects=Sum('course__ects'))['total_ects'] or 0
        total_ects_passed = EnrollmentList.objects.filter(student=student, status='polozen').aggregate(total_ects_passed=Sum('course__ects'))['total_ects_passed'] or 0
        total_ects_left = total_ects - total_ects_passed
        
        # count courses by status
        courses_enrolled = EnrollmentList.objects.filter(student=student, status='upisan').count()
        courses_passed = EnrollmentList.objects.filter(student=student, status='polozen').count()
        courses_lost_signature = EnrollmentList.objects.filter(student=student, status='izgubljen_potpis').count()
    else:
        return HttpResponse("Access Denied!")
    return render(request, 'enrollment_list.html', {
        'student': student, 
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses,
        'block_disenroll_courses': block_disenroll_courses,
        'block_enroll_courses': block_enroll_courses,
        'total_ects': total_ects,
        'total_ects_passed': total_ects_passed,
        'total_ects_left': total_ects_left,
        'courses_enrolled': courses_enrolled,
        'courses_passed': courses_passed,
        'courses_lost_signature': courses_lost_signature,
    })

@login_required
def enroll_course(request, student_id, course_id):
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.STUDENT and request.user.id == student_id:
        student = MyUser.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        # block enroll for 3rd/4rd year courses if not all courses from 1st year are passed
        if student.status == 'redovni':
            higher_year_courses_ids = Course.objects.filter(Q(semester_ft=5) | Q(semester_ft=6)).values_list('id', flat=True)
            first_year_courses_left = EnrollmentList.objects.filter(Q(student=student) & Q(Q(course__semester_ft=1) | Q(course__semester_ft=2)) & ~Q(status='polozen'))
        else:
            higher_year_courses_ids = Course.objects.filter(Q(semester_pt=5) | Q(semester_pt=6) | Q(semester_pt=7) | Q(semester_pt=8)).values_list('id', flat=True)
            first_year_courses_left = EnrollmentList.objects.filter(Q(student=student) & Q(Q(course__semester_pt=1) | Q(course__semester_pt=2)) & ~Q(status='polozen'))
        if first_year_courses_left and course_id in higher_year_courses_ids:
            return HttpResponse("Enroll Not Possible! Courses from 1st year left!")
        else:
            EnrollmentList.objects.create(student=student, course=course)
        
    else:
        return HttpResponse("Access Denied!")
    return redirect('enrollment_list', student_id)

@login_required
def disenroll_course(request, student_id, course_id):
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.STUDENT and request.user.id == student_id:
        enrollment_record = EnrollmentList.objects.filter(student_id=student_id, course_id=course_id).first()
        if enrollment_record.status == 'upisan':
            record = EnrollmentList.objects.get(student_id=student_id, course_id=course_id)
            record.delete()
        elif enrollment_record.status=='polozen':
            return HttpResponse("Action Not Possible! Course Passed!")
        else:
            return HttpResponse("Action Not Possible! Lost Signature!")
    return redirect('enrollment_list', student_id)

@login_required
def students_on_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.PROFESSOR and request.user == course.lecturer:
        enrollment_record = EnrollmentList.objects.filter(course=course)
        return render(request,'students_on_course.html', {'enrollment_record': enrollment_record, 'course': course})
    return redirect('all_courses')

@login_required
def students_on_course_filter(request, course_id, status):
    course = Course.objects.get(id=course_id)
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.PROFESSOR and request.user == course.lecturer:
        if status == 'redovni' or status == 'izvanredni':
            # filter - student status
            enrollment_record = EnrollmentList.objects.filter(course=course, student__status=status)
        else:
            # filter - course status
            enrollment_record = EnrollmentList.objects.filter(course=course, status=status)
        return render(request,'students_on_course.html', {'enrollment_record': enrollment_record, 'course': course})
    return redirect('all_courses')

@login_required
def change_course_status(request, record_id):
    record = EnrollmentList.objects.get(id=record_id)
    course = record.course
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.PROFESSOR and request.user == course.lecturer:
        if request.method == 'GET':
            courseStatusForm = CourseStatusForm(instance=record)
            return render(request, 'change_course_status.html', {'form': courseStatusForm, 'record': record})
        elif request.method == 'POST':
            courseStatusForm = CourseStatusForm(request.POST, instance=record)
            if courseStatusForm.is_valid():
                courseStatusForm.save()
                return redirect('students_on_course', course.id)
            else:
                return HttpResponse("Submit Failure! Invalid Form!")
    else:
        return HttpResponse("Access Denied!")