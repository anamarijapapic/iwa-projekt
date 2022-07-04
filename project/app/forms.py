from django.forms import ModelForm
from .models import Course, MyUser, Role
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
        self.fields['lecturer'].queryset = MyUser.objects.filter(role_id__role=Role.PROFESOR)
        self.fields['program'].required = False
        self.fields['lecturer'].required = False