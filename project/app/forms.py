from django.forms import ModelForm
from .models import Course, MyUser, Role
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'program', 'ects', 'semester_ft', 'semester_pt', 'elective', 'lecturer']
        labels = {
            'ects': _('ECTS'),
            'semester_ft': _('Semester (full-time student)'), 
            'semester_pt': _('Semester (part-time student)'),
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['lecturer'].queryset = MyUser.objects.filter(role_id__role=Role.PROFESSOR)
        self.fields['program'].required = False
        self.fields['lecturer'].required = False

class MyUserEditForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ["username", "email", 'first_name', 'last_name', "role", "status"]
        exclude = ["password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(MyUserEditForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class StudentForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ["username", "email", 'first_name', 'last_name', "password1", "password2", "role", "status"]

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['role'].queryset = Role.objects.filter(role=Role.STUDENT)
        self.fields['status'].choices = (('redovni', 'redovni student'), ('izvanredni', 'izvanredni student'), )

class ProfessorForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ["username", "email", 'first_name', 'last_name', "password1", "password2", "role", "status"]

    def __init__(self, *args, **kwargs):
        super(ProfessorForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['role'].queryset = Role.objects.filter(role=Role.PROFESSOR)
        self.fields['status'].choices = (('none', 'None'), )