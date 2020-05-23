import string
import random
import time 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import LoginForm,RegForm,ChangeNicknameForm,BindEmailForm,ChangePasswordForm,ForgotPasswordForm
from .models import Profile



def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()
    
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html',context)

def wxLogin(request):
    name = request.POST.get('name','')
    password = request.POST.get('password','')
    print(request.POST)
    print(name)
    print(password)
    print("有消息传来")
    islogin=1
    user = auth.authenticate(username=name, password=password)
    if user is None:
        islogin=0
        if User.objects.filter(email=name).exists():
            islogin=1
            username = User.objects.get(email=name).username
            user = auth.authenticate(username=username, password=password)
            if user is None:
                islogin=0

    if islogin==1:
        res1 = res("success","login")
        str1 = stu2dict(res1)
        str2 = stu2dict(res("NB","login"))
        print(str1)
        # a = json.dumps(str1)
        # print(a)
        print(res1)
        data = [str1,str2]
        data = [str1]
        return JsonResponse({"data":data},safe=False)
    else:
        res1 = res("falied","login")
        data = [stu2dict(res1)]
        print(data)
        return JsonResponse({"data":data},safe=False)

class res():
    statue=""
    text=""
    def __init__(self,a,statue):
        if(a=="success"):
            self.statue=1
        else:
            self.statue=0
        self.text = statue+a

def stu2dict(std):
    return{
        'statue':std.statue,
        'text':std.text
    }

def wxRegister(request):
    name = request.POST.get('name','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    print(name)
    print(password)
    # post_data = request.body.decode('utf-8')
    # post_data = json.loads(post_data)
    # name = post_data.get('name')
    # password = post_data.get('password')
    isregister=0
    if not User.objects.filter(username=name).exists():
        user = User.objects.create_user(name, email, password)
        user.save()
        isregister=1

    if isregister==0:
        res1 = res("failed","register")

        data = [stu2dict(res1)]
    else:
        res1 = res("success","register")
        data = [stu2dict(res1)]
    return JsonResponse({'data': data}, safe=False)



def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清除session
            # del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from',reverse('home')))

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html',context)

def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '1074603851@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def forgot_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)