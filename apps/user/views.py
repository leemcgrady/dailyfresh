from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings

from user.models import User, Address, AddressManager
from utils.mixin import LoginRequiredMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django_redis import get_redis_connection
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth.hashers import check_password,make_password
import re
# Create your views here.

def register(request):
    '''注册'''
    if request.method == 'GET':
        # 显示注册页面
        # return render(request, '哈哈哈')
        return render(request, 'register.html')
    else:
        user_name = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([user_name, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user = None

        if user:

            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        user = User.objects.create_user(user_name, password, email)
        user.password = make_password(password)
        user.is_active = 0
        user.save()

        return redirect(reverse('goods:index'))


class RegisterView(View):

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):

        user_name = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([user_name, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        user = User.objects.create_user(user_name, password, email)
        user.password = make_password(password)
        user.is_active = 0
        user.save()

        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"confirm" : user.id}
        token = serializer.dumps(info)
        token = token.decode()

        send_register_active_email.delay(email, user_name, token)

        return redirect(reverse('goods:index'))


class ActiveView(View):

    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.load(token)

            user_id = info["confirm"]

            user = User.objects.get(id = user_id)

            user.is_active = 1

            user.save()

            return redirect(reverse("user:login"))
        except SignatureExpired as e:

            return HttpResponse("激活链接已过期")


class LoginView(View):

    def get(self, request):

        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username' : username, 'checked' : checked})


    def post(self, request):

        user_name = request.POST.get("username")
        password = request.POST.get("pwd")

        if not all([user_name, password]):
            return render(request, "login.html", {"errmsg" : "数据不完整"})

        try:
            user = User.objects.get(username = user_name)
            pwd = user.password

            if check_password(password, pwd):

                if user.is_active:

                    login(request, user)

                    next_url = request.GET.get("next", reverse("goods:index"))

                    response = redirect(next_url)

                    remeber = request.POST.get("remeber")

                    if remeber == 'on':
                        response.set_cookie("username", user_name, max_age=7 * 24 * 3600)
                    else:
                        response.delete_cookie("username")

                    return response
                else:
                    return render(request,'login.html', {"errmsg" : "请激活用户"})

        except User.DoesNotExist:
            return render(request,'login.html', {"errmsg" : "用户不存在"})



class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect(reverse('goods:index'))

class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):

        user = request.user

        address = Address.objects.get_default_address(user)

