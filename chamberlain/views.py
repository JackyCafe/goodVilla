import json
import sys
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from chamberlain.forms import UserRegistrationForm, LoginForm, AttendanceForm
from django.contrib.auth.models import User

import logging

# Create your views here.

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s ',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[
                        logging.FileHandler("mylog.log"),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )


def index(request):
    return render(request, 'account/index.html')


def register(request):
    '''註冊'''
    user_form: UserRegistrationForm
    new_user: User
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('chamberlain:index')

        else:
            return HttpResponse(user_form.errors)
    else:
        user_form = UserRegistrationForm
    return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    form: LoginForm
    user: User
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password']
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['user'] = user.user_id
                    return redirect('chamberlain:attendance')
        else:
            logging.info(form.errors)

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def attendance_view(request):
    user_id = request.session['user']
    form: AttendanceForm
    if request.method == 'POST':
        form = AttendanceForm(request.POST,{'user':user_id})
        if form.is_valid():
            new_action = attendance_view()
            logging.info(new_action)
        else:
            logging.info(form.errors)
    else:
        #form = AttendanceForm(initial={'user_id': user_id})
        form = AttendanceForm({'user':user_id})
    return render(request, 'account/attendance.html', {'form': form})
