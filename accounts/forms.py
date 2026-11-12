from typing import Any
from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,UserChangeForm,SetPasswordForm,PasswordResetForm
from django import forms
from django.contrib.auth import get_user_model

from .models import Profile
from phonenumber_field.formfields import PhoneNumberField as PhoneNumberFormField

class UserProfileForm(forms.ModelForm):
    phone_number = PhoneNumberFormField(region='US')  # Adjust default region as needed

    class Meta:
        model = Profile
        fields = ['phone_number']


class EmailAuthenticationForm(AuthenticationForm):
   # email = forms.EmailField(label='Email', required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

        
        

        self.fields['username']=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
        self.fields['username'].label = ''
        #self.fields['username'].widget.attrs.update({
         #   'class': 'form-control',
          #  'placeholder': 'Email',  
        #})

        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',  
        })

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    

class UserRegisterForm(UserCreationForm):

    first_name=forms.CharField(max_length=20,label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name =forms.CharField(max_length=20,label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email =forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
        
        
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name','email','password1','password2',)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        # self.fields['username'].widget.attrs['class'] = 'form-control'
        # self.fields['username'].widget.attrs['placeholder'] = 'Username'
        # self.fields['username'].label = ''
        # self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        # self.fields['password1'].help_text = '<ul  class="help-text-fr form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password1'].help_text = '<span style="color : white !important;" class="form-text text-muted"><small>Your password must contain at least 8 characters</small></span>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span style="color : white !important;" class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UserUpdateForm(UserChangeForm):
    first_name=forms.CharField(max_length=30,required=True,label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name =forms.CharField(max_length=30,required=True, label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email =forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    username =forms.CharField(label='username',required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    password=None
        
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name','email','username')
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Make the username field uneditable (readonly)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

class UserUpadetEmailForm(UserChangeForm):
    email =forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = None
    
    
    class Meta:
        model = get_user_model()
        fields = ('email',)

class SetPasswordForm1(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm1, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-white text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['new_password1'].widget.attrs['style'] = 'color:white;'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-white text-muted"><small>Enter the same password as before, for verification.</small></span>'
        self.fields['new_password2'].widget.attrs['style'] = 'color:white;'

class PasswordResetForm1(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm1, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'