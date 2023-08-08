# forms.py
from django import forms

class UploadFileForm(forms.Form):
    upload = forms.FileField(label='Select a file', help_text='Allowed formats: .csv')
