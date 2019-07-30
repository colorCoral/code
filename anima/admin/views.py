from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth

from project import models
from project import form
from project import page


# 以下创建视图函数


# 注册  http://127.0.0.1:8000/anm/h_register/
def register(request):

    if request.method == 'GET':
        form_obj = form.UserForm
        return render(request, 'admin/register.html', {'form_obj': form_obj})
    else:
        form_obj = form.UserForm(request.POST)

        if form_obj.is_valid():
            data = form_obj.cleaned_data
            data.pop('r_password')
            models.UserInfo.objects.create_user(**data)
            return redirect('login')
        else:
            return render(request, 'admin/h_index.html', {'form_obj': form_obj})


# 后端登录 mycolor1  130928asd
def login(request):

    response_msg = {'code': None, 'msg': None}
    if request.method == 'GET':
        return render(request, "admin/login.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # valid_code = request.POST.get('valid_code')
        valid_code = '1111'

        # 后端暂时不调用验证码，后期加上
        # if valid_code.upper() == request.session.get('valid_str').upper():
        if valid_code.upper() == '1111':
            # 这里auth是django提供的方法，用来检验用户名和密码
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                # 这里使用了auth方法，自动添加了session
                auth.login(request, user_obj)
                response_msg['code'] = 1000
                response_msg['msg'] = '登录成功'
                request.session['username'] = username
                # 暂时不打开，后期权限
                # initial_session(request, user_obj)
            else:
                response_msg['code'] = 1001
                response_msg['msg'] = '用户名或者密码错误'
        else:
            response_msg['code'] = 1001
            response_msg['msg'] = '验证码错误'

    return JsonResponse(response_msg)


# 后台首页,前段验证成功跳转到这里
def h_index(request):

    if request.method == 'GET':
        username = request.session.get('username')
        response_msg = {'name': username, 'msg': None}
        return render(request, 'admin/h_index.html', {'response_msg': response_msg})


def h_user(request):

    current_page_num = request.GET.get('page', 1)
    all_user = models.UserInfo.objects.filter()
    total_counts = all_user.count()
    page_obj = page.PageNation(request.path, current_page_num, total_counts,request)
    all_user = all_user[page_obj.start_num:page_obj.end_num]
    ret_html = page_obj.page_html()

    return render(request, 'admin/h_user.html', {'all_user': all_user, 'ret_html': ret_html})



