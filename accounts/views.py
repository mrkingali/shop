from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from utils import send_top_code
from .models import OtpCode, User
from random import randint

from .forms import UserRegistrationForm, VerifyCodeForm


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
    class_form = VerifyCodeForm

    def get(self, request):
        form = self.class_form
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])

        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create(phone_number=user_session['phone_number']
                                    , email=user_session['email']
                                    , full_name=user_session['full_name']
                                    , password=user_session['password'])
                code_instance.delete()
                messages.success(request, "you registered successfully", 'success')
                return redirect("home:home")
            else:
                messages.error(request, 'code was incorrect', 'danger')
                return redirect('accounts:verify_code')
        else:
            messages.error(request, 'form got error', 'danger')
            return redirect("home:home")
