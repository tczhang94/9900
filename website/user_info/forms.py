from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username/Email',
                               widget=forms.TextInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your username or email',
                                     'required': True}),
                               min_length=3)

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your password',
                                     'required': True}),
                               max_length=16, min_length=3)

    def clean(self):

        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data

            raise forms.ValidationError('Wrong username/password')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


# 注册
class RegForm(forms.Form):

    username = forms.CharField(label='Userame',
                               widget=forms.TextInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your username',
                                     'required': True}),
                               max_length=16, min_length=3)

    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your password',
                                     'required': True}),
                               max_length=16, min_length=3)

    confirm_password = forms.CharField(label='Confirm Password',
                               widget=forms.PasswordInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your password again',
                                     'required': True}),
                               max_length=16, min_length=3)

    email = forms.EmailField(label='Email',
                                widget=forms.EmailInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input email address',
                                    'required': True}))

    verification_code = forms.CharField(
                                label='Verify Code',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Please press send code to receive verify code',
                                    'required': True}
                                )
                            )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):

        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exises')

        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Different passwords are input, try again')

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email has been registered')

        # 判断验证码是否正确
        code = self.request.session.get('register_email_code', '').lower()
        verification_code = self.cleaned_data.get('verification_code', '').strip().lower()
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('Wrong verify code')

        return self.cleaned_data


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='Nickname',
                               widget=forms.TextInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your nickname'}),
                                   max_length=15)

    def __init__(self,*args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm,self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('You did not log in yet')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == '':
            raise ValidationError("Empty New Nickname")
        return nickname_new


class ChangePwdForm(forms.Form):

    old_pwd = forms.CharField(label='Old Password',
                               widget=forms.PasswordInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your original password'}),
                               max_length=16, min_length=3)
    new_pwd = forms.CharField(label='New Password',
                               widget=forms.PasswordInput(attrs=
                                    {'class': 'form-control', 'placeholder': 'Please input your new password'}),
                               max_length=16, min_length=3)

    def clean(self):
        new_pwd = self.cleaned_data.get('new_pwd','')
        if new_pwd == '':
            raise forms.ValidationError('Password cannot be empty')

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePwdForm, self).__init__(*args,**kwargs)

    def clean_old_pwd(self):
        old_pwd = self.cleaned_data.get('old_pwd','')
        if not self.user.check_password(old_pwd):
            raise ValidationError('Wrong original password')
        return old_pwd


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
           attrs={'class': 'form-control','placeholder': 'Please input correct email address',
                  'required': True}
       )
    )

    verification_code = forms.CharField(
        label='Verify Code',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Please press send code to receive verify code',
                   'required': True}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断是否登陆
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('You did not log in yet')

        # 判断邮箱是否已经绑定
        if self.request.user.email != '':
            raise forms.ValidationError('Already bind email')

        # 判断验证码是否正确
        code = self.request.session.get('bind_email_code', '').lower()
        verification_code = self.cleaned_data.get('verification_code','').strip().lower()
        if not(code != '' and code == verification_code):
            raise forms.ValidationError('Wrong verify code')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email has been bind')
        return email


class ForgotPwdForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Please enter your bound email',
                   'required': True}
        )
    )

    verification_code = forms.CharField(
        label='Verify Code',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Please press send code to receive verify code',
                   'required': True}
        )
    )

    new_pwd = forms.CharField(label='New Password',
                              widget=forms.PasswordInput(attrs=
                                                         {'class': 'form-control',
                                                          'placeholder': 'Please input your new password',
                                                          'required': True}),
                              max_length=16, min_length=3)

    confirm_new_pwd = forms.CharField(label='Confirm New Password',
                              widget=forms.PasswordInput(attrs=
                                                         {'class': 'form-control',
                                                          'placeholder': 'Please input your new password again',
                                                          'required': True}),
                              max_length=16, min_length=3)


    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPwdForm, self).__init__(*args, **kwargs)

    def clean(self):

        #判断邮箱是否存在
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email not exists')

        # 判断验证码是否正确
        code = self.request.session.get('forgot_pwd_code', '').lower()
        verification_code = self.cleaned_data.get('verification_code', '').strip().lower()
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('Wrong verify code')

        new_pwd = self.cleaned_data['new_pwd'].strip()
        confirm_new_pwd = self.cleaned_data['confirm_new_pwd'].strip()
        if new_pwd == '':
            raise forms.ValidationError('Password cannot be empty')

        if new_pwd and confirm_new_pwd:
            if new_pwd != confirm_new_pwd:
                raise forms.ValidationError('Different passwords are input, try again')

        return self.cleaned_data
