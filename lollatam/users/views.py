from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from users.forms import UserForm, AuthForm
from users.models import Profile

from lollatam.settings import EMAIL_HOST_USER

import secrets


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

        # Check for form validation including username and email repeated.
        if form.is_valid():
            
            user = form.save()

            # Create a new profile for the user
            profile = Profile(user=user, username=user.username)
            profile.save()

            # Generate a verification token and save it to the profile
            token = secrets.token_hex(32)
            profile.verification_token = token
            profile.save()

            # Send a verification email
            subject = 'Verifica tu correo electrónico'
            message = f'Hola {user.username},\n\nPor favor haz clic en el siguiente enlace para verificar tu correo electrónico:\n\nhttp://{request.get_host()}/users/verify-email/?token={token}'
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            login(request, user)

            return HttpResponseRedirect(reverse('network:profile'))
        else:
            return render(request, 'users/signup.html', {'form': form})

    context['form'] = UserForm()

    return render(request, 'users/signup.html', context)

@login_required
def verify_email(request):

    token = request.GET.get('token')

    if token is not None:

        try:
            profile = Profile.objects.get(verification_token=token)
            profile.email_verified = True
            profile.verification_token = None
            profile.save()
        except Profile.DoesNotExist:
            pass

    return HttpResponseRedirect(reverse('network:profile'))
