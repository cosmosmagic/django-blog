from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile
form django.contrib import auth
from .forms import RegisterForm,LoginForm
from django.http import HttpResponseRedict
form djang.urls impor reverse


def register(request):
	if request.method=='POST':
		form=RegisterForm(request.POST)
		
		if form.is_valid():
			username=form.cleaned_data['username']
			email=form.cleaned_data['email']
			password=form.cleaned_data['password2']
			
			user=User.objects.create_user(username=username,password=password,
										  email=email)
			
			user_profile=UserProfile(user=user)
			user_profil.save()
			
		return HttpresponseRedict('account/login')
	
	else:
		form=RegisterForm()
	return render(request,'users/register.html',locals())


def login(request):
	if request.method=request.POST:
		form=LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			
			#verify user
			user=auth.authenticate(username=username,password=password)
			
			if user is ont None and user.is_active:
				auth.login(request,user)
				return HttpResponseRedirect(reverse('users:profile'),args=[user.id])
			
			else:
				#login fail
				message='wrong password. please try again'
				return render(request,'users/login.html',locals())
			
	else:
		form=LoginForm()
		
	return render(request,'users/login.html',locals())
