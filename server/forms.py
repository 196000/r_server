from django import forms
from django.contrib.auth.models import User
from server.models import File

class FileForm(forms.ModelForm):
    file = forms.FileField()
    class Meta:
        model = File
        exclude = []
		
class StudyForm(forms.Form):
    study = forms.CharField(label = 'New Study', max_length = 100, min_length = 2)
