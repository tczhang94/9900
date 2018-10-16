import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePwdForm, ForgotPwdForm
from django.contrib.auth.models import User
from .models import Profile
from django.http import JsonResponse
from django.core.mail import send_mail

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    # 提交数据 login验证 操作
    if request.method == 'POST':

        # 带提交数据 错误的话forms.clean会处理
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    # 加载数据
    else:
        # 空的
        login_form = LoginForm()

    context = dict()
    context['login_form'] = login_form
    return render(request, 'login.html', context)


# 如果post 取出来实例化 不是post直接实例化
def register(request):

    if request.method == 'POST':

        # 带提交数据 错误的话forms.clean会处理
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():

            # 获取三个参数
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']

            # 创建注册实例化
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # 清除session
            del request.session['register_email_code']

            # 直接登陆
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        reg_form = RegForm()

    context = dict()
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


def user_info(request):
    context = {}
    return render(request, 'user_info.html',context)


def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created =Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect('user_info')
    else:
        form = ChangeNicknameForm()
    context = dict()
    context['change_nickname'] = form
    return render(request, 'change_profile.html',context)


def change_pwd(request):
    if request.method == 'POST':
        form = ChangePwdForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_pwd = form.cleaned_data['old_pwd']
            new_pwd = form.cleaned_data['new_pwd']
            user.set_password(new_pwd)
            user.save()
            auth.logout(request)

            return redirect('home')
    else:
        form = ChangePwdForm()
    context = dict()
    context['change_pwd'] = form
    return render(request, 'change_pwd.html',context)


# request=request
def bind_email(request):

    if request.method == 'POST':

        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():

            email = form.cleaned_data['email']

            request.user.email = email
            request.user.save()

            # 清除session
            del request.session['bind_email_code']

            return redirect('user_info')
    else:
        form = BindEmailForm()

    context = dict()
    context['form'] = form
    return render(request, 'bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = dict()

    if email != '':
        # make the code
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # send the code
            send_mail(
                'Fake leg',
                'From Fake Leg Official: Hi dear user, the verify code is: %s' % code,

                '522366853@qq.com',

                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def forgot_pwd(request):
    if request.method == 'POST':

        form = ForgotPwdForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_pwd']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # 清除session
            del request.session['forgot_pwd_code']

            # 直接登陆
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ForgotPwdForm()

    context = dict()
    context['form'] = form
    return render(request, 'forgot_pwd.html', context)
