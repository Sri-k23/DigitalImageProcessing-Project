from django import forms
from .models import Sampleapp


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Sampleapp
        fields = ['name', 'emp_image']
