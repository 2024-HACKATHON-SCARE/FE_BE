from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    is_child = forms.BooleanField(required=True, label='자녀')
    is_parent = forms.BooleanField(required=True, label='부모')
    
    class Meta():
        model = get_user_model()
        fields = ['username', 'email', 'is_child', 'is_parent']