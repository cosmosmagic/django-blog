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
