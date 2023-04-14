import logging

from django import  forms
from django.contrib.auth.models import User
import sys
from chamberlain.models import Attendance

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
    def __init__(self, *args, **kwargs):
        super(AttendanceForm,self).__init__()
        # initial = kwargs.get("initial",{})
        # user =initial.get('user_id')
        # self.fields['user'].initial = user
        # self.fields['user'].widget.attrs['disable'] = True
        user = forms.CharField()
        # logging.info(user)

    class Meta:
        model = Attendance
        exclude =('user',)