from django.shortcuts import render, HttpResponse, redirect
from project import form
from project import models

# Create your views here.


def register(request):

    if request.method == 'GET':
        form_obj = form.UserForm()
        return render(request, 'home/register.html', {'form_obj': form_obj})
    else:
        form_obj = form.UserForm(request.POST)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            data.pop('r_password')
            models.UserInfo.objects.create_user(**data)
            return redirect('logo')
        else:
            return render(request, 'home/register.html', {'form_obj': form_obj})


def login(request):

    request_msg = {'code': None, 'msg': None}
    if request.method == 'GET':
        return render(request, 'home/login.html', {'request_msg': request_msg})
    else:
        return HttpResponse('post ok')
