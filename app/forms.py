from django import forms

class EnfermedadForm(forms.Form):
    enfermedad = forms.CharField(label='Your name', max_length=100)