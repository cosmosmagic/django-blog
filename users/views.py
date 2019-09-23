from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from .forms import RegisterForm, LoginForm, ProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import hashlib


def hash_code(s, salt='register'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            hash_password = hash_code(password)

            new_user = User()
            new_user.username = username
            new_user.email = email
            new_user.password = password
            new_user.save()

            user_profile = UserProfile(user=new_user)
            user_profile.save()

        return HttpResponseRedirect(reverse('users:login'))
    else:
        form = RegisterForm()
        return render(request, 'users/register.html', locals())


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'), args=[user.id])

            else:
                message = 'wrong password. please try again'
                return render(request, 'users/login.html', locals())
    else:
        form = LoginForm()
    return render(request, 'users/login.html', locals())


# user information
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', locals())


# change user information
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()
            return HttpResponseRedirect(reverse('users:profile'), args=[user.id])
    else:
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user_profile.org,
            'telephone': user_profile.telephone,
        }
        form = ProfileForm(default_data)

    return render(request, 'users:profile_update.html', locals())
