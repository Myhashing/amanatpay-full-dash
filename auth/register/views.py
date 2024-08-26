from django.contrib.auth.models import  Group
from django.contrib import messages
from django.utils import timezone
from auth.views import AuthView
from auth.helpers import send_otp, encrypt_otp
from auth.models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


class RegisterView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")  # Replace 'index' with the actual URL name for the home page

        return super().get(request)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")  # Capture mobile number
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلا در سیستم ثبت شده است.")
            return redirect("register")
        elif email and User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلا در سیستم ثبت شده است.")
            return redirect("register")
        elif User.objects.filter(profile__mobile=mobile).exists():
            messages.error(request, "این شماره موبایل قبلا در سیستم ثبت شده است.")
            return redirect("register")

        created_user = User.objects.create_user(username=username, email=email, password=password)
        created_user.save()

        user_group, created = Group.objects.get_or_create(name="client")
        created_user.groups.add(user_group)

        user_profile, created = Profile.objects.get_or_create(user=created_user)
        user_profile.mobile = mobile  # Save mobile number to profile
        user_profile.email = email
        user_profile.save()

        otp_code = send_otp(mobile)  # Send OTP to user's mobile number
        expiration_time = timezone.now() + timezone.timedelta(minutes=10)
        request.session['encrypted_otp'] = encrypt_otp(otp_code)
        request.session['mobile'] = mobile
        request.session['username'] = username
        request.session['otp_expiration_time'] = expiration_time.isoformat()

        return redirect("verify-otp")  # Redirect to OTP verification page
