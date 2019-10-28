from django import forms
from django.contrib.auth.models import User


class UserRegitrationForm(forms.Form):
    username = forms.CharField(
                            label="Username",
                            max_length=100,
                            min_length=5,
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(
                            label='Email',
                            max_length=100,
                            min_length=5,
                            widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(
                            label="Password",
                            max_length=100,
                            min_length=5,
                            widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(
                            label="Confirm Password",
                            max_length=100,
                            min_length=5,
                            widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("The email is already registered")
        return email

    """def clean_password1(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('The passwords do not match.')
        return password1"""


    """def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('This password does not match the above.')
        return password2"""
    
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('The passwords do not match')
        

    def clean_username(self):
        uname = self.cleaned_data['username']
        qs = User.objects.filter(username=uname)
        if qs.exists():
            raise forms.ValidationError(f'The username {uname} is already registered')
        return uname