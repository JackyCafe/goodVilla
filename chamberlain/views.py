import json
import sys
from datetime import datetime, timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sessions import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from chamberlain.forms import UserRegistrationForm, LoginForm, AttendanceForm
from django.contrib.auth.models import User

import logging

# Create your views here.
from chamberlain.models import MajorItem, DetailItem, Attendance

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


@login_required
def dashboard(request):
    request.session['user'] = request.user.id
    return render(request,
                  'account/dashboard.html',
                  )


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
                    return redirect('chamberlain:index')
        else:
            logging.info(form.errors)

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def attendance_view(request):
    return HttpResponse('媽～我在這裡')


def major(request):
    user_id = request.session['user']
    items = MajorItem.objects.all()
    return render(request, 'account/major.html', {'items': items})


def detail(request, id):
    items = get_list_or_404(DetailItem, major_id=id)
    return render(request, 'account/detail.html', {'items': items})


def task_end(request,id):
    task = get_object_or_404(Attendance, id = id)
    task.end_time = datetime.now(timezone.utc)
    task.spend_time = (task.end_time-task.start_time).total_seconds()/60
    task.save()

    return redirect('chamberlain:major')


def task_record(request, id):
    user_id = request.session['user']
    user = User.objects.get(id=user_id)
    items = get_object_or_404(DetailItem,id = id)

    new_task = Attendance(user=user,
                          items=items,
                          content=items.detail,
                          start_time=datetime.now(timezone.utc))
    new_task.save()
    return render(request,'account/operation_time.html',{'task':new_task})

    # form: AttendanceForm
    # if request.method == 'POST':
    #     form = AttendanceForm(request.POST)
    #     if form.is_valid():
    #         new_action = form.save()
    #         logging(new_action)
    #         # new_action.save()
    #     else:
    #         print(form.errors)
    # else:
    #     form = AttendanceForm(initial={'user': user_id, 'items': id, 'content': items.detail })
    #
    # return render(request, 'account/attendance.html', {'form': form})
