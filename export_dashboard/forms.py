from django import forms

class ExcelUploadForm(forms.Form):
    product = forms.CharField(max_length=200)
    excel_file = forms.FileField()