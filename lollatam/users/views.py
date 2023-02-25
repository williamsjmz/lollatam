from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

from users.models import User

import re
import datetime

# Error messages
INVALID_FIRST_LAST_NAME_MESSAGE = 'Nombre o apellido inválido. Los campos nombre y apellido sólo pueden contener caracteres del abecedario, acentos o espacios (50 caracteres máximo).'
INVALID_BIRTHDAY_MESSAGE = 'Fecha de nacimiento inválida.'
INVALID_USERNAME_MESSAGE = 'Nombre de usuario inválido. El campo nombre de usuario sólo puede contener caracteres alfanuméricos, puntos y guiones bajos (50 caracteres máximo).'
INVALID_EMAIL_MESSAGE = 'Correo electrónico inválido. El correo electrónico debería tener el formato: \'ejemplo@dominio.com\'.'
INVALID_PASSWORD_MESSAGE = 'Contraseña inválida. Las contraseñas no coinciden o no se ingreso un valor (25 caracteres máximo).'

def login_page(request):
    return render(request, 'users/login.html')

def logout_page(request, user_id):
    return HttpResponse(f'Vista de cierre de sesión para el usuario con ID {user_id}.')

# Registration view
def signup(request):

    # Context for signup template
    context = {}

    if request.method == 'POST':
        
        # Get data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birthday = request.POST.get('birthday')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        # Response messages
        error_messages = []

        # Validates first and last names
        if (not re.match('^[a-zA-ZÀ-ÿ00f100d1 ]{1,50}$', first_name)) or (not re.match('^[a-zA-ZÀ-ÿ00f100d1 ]{1,50}$', last_name)):
            error_messages.append(INVALID_FIRST_LAST_NAME_MESSAGE)

        # Validates username
        if not re.match('^[a-zA-Z0-9_.]{1,50}$', username):
            error_messages.append(INVALID_USERNAME_MESSAGE)

        # Validates birthday
        if not birthday or datetime.datetime.strptime(birthday, '%Y-%m-%d') > datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d'):
            error_messages.append(INVALID_BIRTHDAY_MESSAGE)

        # Validates email
        if not re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
            error_messages.append(INVALID_EMAIL_MESSAGE)

        # Validates password
        if (not password or not password_confirmation) or (password != password_confirmation) or (len(password) > 25):
            error_messages.append(INVALID_PASSWORD_MESSAGE)

        # If there are not errors
        if not error_messages:

            # Attempt to create a new user
            try:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    birthday=birthday,
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
            except IntegrityError as e:
                return render(request, 'users/signup.html', {
                    'message': 'Ya existe una cuenta con el correo electrónico o nombre de usuario proporcionados.'
                })
            
            # Login the user
            login(request, user)

            # Redirect user to his profile
            return HttpResponseRedirect(reverse('network:profile'))
        
        else:
            context['error_messages'] = error_messages

    return render(request, 'users/signup.html', context)