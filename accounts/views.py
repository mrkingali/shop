from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from utils import send_top_code
from .models import OtpCode
from random import randint

from .forms import UserRegistrationForm


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            random_code = randint(1000, 9999)
            send_top_code(cd['phone'], random_code)
            OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password'],
            }
            messages.success(request, 'we send message to you', 'success')
            return redirect("accounts:verify_code")
        return redirect("home:home")


class UserRegisterVerifyCodeView(View):


    def get(self, request):
        pass



    def post(self, request):
        pass
