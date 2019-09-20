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
