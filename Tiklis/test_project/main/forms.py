# forms.py
from django import forms

class UploadFileForm(forms.Form):
    upload = forms.FileField(label='Select a file', help_text='Allowed formats: .csv')

class UserInputForm(forms.Form):
    date = forms.DateField(label="Date (YYYY-MM-DD)")
    commodity = forms.CharField(max_length=100, label="Commodity")
    variety = forms.CharField(max_length=100, label="Variety")
    classification = forms.CharField(max_length=100, label="Classification")
    category = forms.CharField(max_length=100, label="Category")
    time = forms.TimeField(label="Time")