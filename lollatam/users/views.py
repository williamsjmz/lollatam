from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

from users.forms import UserForm

def login_page(request):

    if request.method == 'POST':

        # Get data from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('network:profile'))
        else:
            return render(request, 'users/login.html', {'error_messages': [INVALID_CREDENTIALS]})

    return render(request, 'users/login.html')

def logout_page(request, user_id):
    return HttpResponse(f'Vista de cierre de sesión para el usuario con ID {user_id}.')

# Registration view
def signup(request):

    # Context for signup template
    context = {}

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            # Attempt to create a new user
            try:
                user = form.save()
            except IntegrityError as e:
                return render(request, 'users/signup.html', {
                    'message': 'Ya existe una cuenta con el correo electrónico o nombre de usuario proporcionados.'
                })
            # Login the user
            login(request, user)

            # Redirect user to his profile
            return HttpResponseRedirect(reverse('network:profile'))
        
        else:
            return render(request, 'users/signup.html', {'form': form})
    

    context['form'] = UserForm()

    return render(request, 'users/signup.html', context)