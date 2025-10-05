from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate , login
from django.forms import ValidationError

class LoginForm(AuthenticationForm):
    
    username = forms.EmailField(max_length=30 , required = True , label='Email Address')

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                result = authenticate(username=user.username, password=password)
                
                if result is not None:
                    self.user_cache = result
                    return self.cleaned_data
                else:
                    raise ValidationError("Email or Password invalid")
            except User.DoesNotExist:
                raise ValidationError("Email or Password invalid")
        
        return self.cleaned_data
        