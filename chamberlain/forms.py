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
    def __init__(self, *args, **kwargs):
        super(AttendanceForm,self).__init__()
        initial = kwargs.get("initial",{})
        items = initial.get('items')
        content = initial.get('content')
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['items'].initial = items
        self.fields['content'].initial = content
        self.fields['start_time'].initial = datetime.now()

        # logging.info(user)

    class Meta:
        model = Attendance
        exclude =('user',)



