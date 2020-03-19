from django import forms

class UserLoginForm(forms.Form):
    """Form to login user"""
    username = forms.CharField(
        label="Enter Username",
        widget=forms.TextInput(attrs={'class':'form-control w-50 d-inline-block'}))
    password = forms.CharField(
        label="Enter Password",
        widget=forms.PasswordInput(attrs={'class':'form-control w-50 d-inline-block'}))    
        