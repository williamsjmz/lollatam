from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User

class UserForm(UserCreationForm):
	'''
	Form that uses built-in UserCreationForm to handle user creation
	'''
	username = forms.CharField(max_length=50, required=True,
	widget=forms.TextInput(attrs={
		'placeholder': 'Nombre de usuario', 
		'name': 'username', 
		'type': 'text', 
		'class': 'form-control'
	}))
	first_name = forms.CharField(max_length=50, required=True,
		widget=forms.TextInput(attrs={
            'placeholder': 'Nombre(s)', 
            'name': 'first_name', 
            'type': 'text', 
            'class': 'form-control'
	    }))
	last_name = forms.CharField(max_length=50, required=True,
		widget=forms.TextInput(attrs={
            'placeholder': 'Apellido(s)', 
            'name': 'last_name', 
            'type': 'text', 
            'class': 'form-control'
	    }))
	email = forms.EmailField(required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Correo electrónico', 
            'name': 'email', 
            'type': 'email', 
            'class': 'form-control'
        }))
	password1 = forms.CharField(max_length=25, required=True,
		widget=forms.PasswordInput(attrs={
		    'placeholder': 'Contraseña', 
            'name': 'password1', 
            'type': 'password', 
            'class': 'form-control'
	    }))
	password2 = forms.CharField(max_length=25, required=True,
		widget=forms.PasswordInput(attrs={
			'placeholder': 'Confirmar contraseña', 
			'name': 'password2', 
			'type': 'password', 
			'class': 'form-control'
		}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )

class AuthForm(AuthenticationForm):
	'''
	Form that uses built-in AuthenticationForm to handle user auth
	'''
	username = forms.CharField(max_length=50, required=True,
		widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario', 
            'name': 'username', 
            'type': 'text', 
            'class': 'form-control'
	    }))
	password = forms.CharField(max_length=25, required=True,
		widget=forms.PasswordInput(attrs={
		    'placeholder': 'Contraseña', 
            'name': 'password', 
            'type': 'password', 
            'class': 'form-control'
	    }))

	class Meta:
		model = User
		fields = ('username','password', )