from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import UserProfile
from .forms import RegisterForm, LoginForm, ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def user_register(request):
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

                new_user = User(
                    username=username,
                    email=email
                )
                new_user.set_password(password2)
                new_user.save()
                user_profile = UserProfile(user=new_user)
                user_profile.save()

                message = 'register success!'
                form = LoginForm()
                return render(request, 'users/login.html', locals())
                # return redirect(reverse('users:login'))
        else:
            return render(request, 'users/register.html')
    form = RegisterForm()
    return render(request, 'users/register.html', locals())


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        message = 'please check your content!'
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('myblog:index'))
            else:
                message = "user or password is incorrect!"
                return render(request, 'users/login.html', locals())

        else:
            message = "user or password is illegal!"
            return render(request, 'users/login.html', locals())
    form = LoginForm()
    return render(request, 'users/login.html', locals())


def user_logout(request):
    logout(request)
    return redirect(reverse('myblog:index'))


# user information
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', locals())


# change user information
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user_id=pk)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']

            if 'avatar' in request.FILES:
                user_profile.avatar = form.cleaned_data['avatar']
            user_profile.save()
            return redirect(reverse('users:profile', args=[user.id]))
    else:
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user_profile.org,
            'telephone': user_profile.telephone,
        }
        form = ProfileForm(default_data)

    return render(request, 'users/profile_update.html', locals())
