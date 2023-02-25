from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from users.forms import UserForm, AuthForm


def login_page(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('network:profile'))

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('network:profile'))
        else:
            return render(request, 'users/login.html', {
                'form': AuthForm(request.POST),
                'error': 'Las credenciales son inválidas.'
            })

    return render(request, 'users/login.html', {
        'form': AuthForm(),
    })

@login_required
def logout_page(request):
        
	logout(request)
	return HttpResponseRedirect(reverse('users:login'))

def signup(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('network:profile'))

    context = {}

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            try:
                user = form.save()
            except IntegrityError as e:
                return render(request, 'users/signup.html', {
                    'message': 'Ya existe una cuenta con el correo electrónico o nombre de usuario proporcionados.'
                })
            
            login(request, user)

            return HttpResponseRedirect(reverse('network:profile'))
        
        else:
            return render(request, 'users/signup.html', {'form': form})
    

    context['form'] = UserForm()

    return render(request, 'users/signup.html', context)