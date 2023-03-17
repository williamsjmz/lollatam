from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed

from users.models import Profile


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            profile = Profile.objects.get(user=request.user)
            context = {
                'email_verified': profile.email_verified,
            }
            return render(request, 'network/profile.html', context)
        else:
            return HttpResponseNotAllowed(['GET'])
    else:
        return HttpResponseRedirect(reverse('users:login'))