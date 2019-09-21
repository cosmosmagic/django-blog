from django import forms
from django.contrib.auth.models import User


def check_email(email):
    pattern=re.compile(r'\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?')
    return re.match(pattern,email)


class RegisterForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=50)
    email=forms.EmailField(label='邮箱')
    password1=forms.CharField(label='密码',widget=forms.PasswordInput)
    password2=forms.CharField(label='密码确认',widget=forms.PasswordIuput)
    
    
    #use clean methods to define custom validation rules
    def clean_username(self):
        username=self.cleaned_data.get('username')
        
        if len(username)<6:
            raise forms.ValidationError('你的用户名必须不小于6位字符')
        elif len(username)>50:
            raise forms.ValidationError('你用户名过长')
        else:
            filter_result=User.objects.filter(username_exact=username)
            if len(filter_result)>0:
                raise forms.ValidationError('用户名已存在')
                
        return username
                
    def clean_email(self):
        email=self.cleaned_data.get('email')
        
        if check_email(email):
            filter_result=User.objects.filter(email__exact=email)
            
            if len(filter_result>0):
                raise forms.ValidationError('your emial has already exists')
                
        else:
            raise forms.ValidationError('please enter a valid emial')
            
        return email
        
    def clean_password1(self):
        password1=self.cleaned_data.get('password1')
        
        if len(password1)<6:
            raise forms.ValidationError('your password is too short')
        elif len(password)>20:
            raise forms.ValidationError('your password is too long')
            
        return password1
    
    def clean_password2(self):
        password2=self.cleaned_data.get('password2')
        password1=self.cleaned_data.get('password1')
        
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError('password mismatch. please enter again')
            
        return password2
    
   
class LoginForm(forms.Form):
	username=forms.CharField(label='用户名',max_length=50)
	password=forms.CharField(label='密码',widget=form.PasswordInput)
	
	#use clean method to define custom validation rules
	def clean_username(self):
		username=self.cleaned_data.get('username')
		filter_result=User.objects.filter(username__exact=username)
		if not filter_result:
			raise form.ValidationError('the username does not exist, please register first.')
			
		return username
	
	
class ProfileForm(forms.Form):
	first_name=forms.CharField(lable='First Name',max_length=50,required=False)
	last_name=forms.CharField(lable='Last Name',max_length=50,required=False)
	org=forms.CharField(label='User',max_length=50,required=False)
	telephone=forms.CharField(label='Telephone',max_length=50,required=False)
