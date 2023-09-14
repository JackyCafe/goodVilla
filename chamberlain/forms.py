import logging
from datetime import datetime

from django import  forms
from django.contrib.auth.models import User
import sys
from chamberlain.models import Attendance, MajorItem

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s ',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[
                        logging.FileHandler("mylog.log"),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )


class LoginForm(forms.Form):
    username = forms.CharField(label='使用者名稱')
    password = forms.CharField(label='使用者密碼', widget=forms.PasswordInput)

    # class Meta:
    #     model = User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='請輸入密碼', widget=forms.PasswordInput)
    password2 = forms.CharField(label='請再次輸入密碼', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('兩次密碼不相同')
        return cd['password2']


class AttendanceForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(AttendanceForm,self).__init__(*args, **kwargs)
        initial = kwargs.get('initial',{})
        data:Attendance = initial.get('data')
        self.fields['user'].initial=data.user
        self.fields['items'].initial = data.items
        self.fields['start_time'].initial = data.start_time
        self.fields['end_time'].initial =data.end_time
        self.fields['spend_time'].initial = data.spend_time
        self.fields['content'].initial = data.content

    class Meta:
        model = Attendance
        fields ='__all__'
        # exclude =('user',)
    def save(self, commit=True):

        obj:Attendance = super(AttendanceForm, self).save(commit=False)
        obj.user = self.cleaned_data['user']
        obj.start_time = self.cleaned_data['start_time']
        obj.end_time = self.cleaned_data['end_time']
        obj.items = self.cleaned_data['items']
        obj.content = self.cleaned_data['content']
        if commit:
            obj.save()
        return obj

class MajorForm(forms.ModelForm):
    class Meta:
        model = MajorItem
        fields = '__all__'


