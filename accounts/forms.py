from django import forms
from .models import Slot


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['start_time', 'end_time', 'fee']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fee in Rs'}),
        }


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ])
