from django.shortcuts import render

# Create your views here.

def index(request):
    # 显示注册页面
    # return render(request, '哈哈哈')
    return render(request, 'index.html')
    # '''注册'''
    # if request.method == 'GET':