from django.shortcuts import render, get_object_or_404, redirect
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


def index(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('users:index'))
    return render(request, 'users/index.html')


def register(request):
    if request.session.get('is_login', None):
        return redirect(reverse('users:index'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            # hash_password = hash_code(password)

            if password1 != password2:
                message = 'two password is inconsistent!'
                return render(request, 'users/register.html', locals())
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:
                    message = 'the username is exist!'
                    return render(request, 'users/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = 'the email is exist!'
                    return render(request, 'users/register.html', locals())

                new_user = User.objects.create(
                    username=username,
                    password=password2,
                    email=email
                )
                user_profile = UserProfile(user=new_user)
                user_profile.save()
                return render(request, 'users/login.html', locals())
        else:
            return render(request, 'users/register.html', locals())
    form = RegisterForm()
    return render(request, 'users/register.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect(reverse('users:index'))
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
            except:
                message = "user doesn't exist!"
                return render(request, 'users/login.html')
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect(reverse('users:index'))
            else:
                message = 'password is incorrect'
                return render(request, 'users/login.html', locals())
        else:
            return render(request, 'users/login.html', locals())
    form = LoginForm()
    return render(request, 'users/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('users:login'))
    request.session.flush()
    return redirect(reverse('users:login'))


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
