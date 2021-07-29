from django import forms
from django.contrib.auth.forms import  UserCreationForm
from user.models import CustomUser, Customer
from django.core.exceptions import ValidationError

class RegistrationAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_2', )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            raise ValidationError("Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

