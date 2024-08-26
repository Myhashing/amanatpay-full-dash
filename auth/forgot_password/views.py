from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from auth.helpers import send_password_reset_email, send_otp, encrypt_otp
from auth.models import Profile  # Import the Profile model
from auth.views import AuthView
from datetime import timedelta, datetime
import uuid
from django.utils import timezone


class ForgetPasswordView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("index")  # Replace 'index' with the actual URL name for the home page

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        contact_info = request.POST.get('contact')  # Make sure to fetch the input correctly

        if not contact_info:
            messages.error(request, "لطفاً ایمیل یا شماره موبایل خود را وارد کنید.")
            return redirect("forgot-password")

        # Email case
        if "@" in contact_info:
            user = User.objects.filter(email=contact_info).first()
            if not user:
                messages.error(request, "کاربری با این ایمیل وجود ندارد.")
                return redirect("forgot-password")

            # Generate token and send email
            token = str(uuid.uuid4())
            expiration_time = datetime.now() + timedelta(hours=24)

            user_profile, created = Profile.objects.get_or_create(user=user)
            user_profile.forget_password_token = token
            user_profile.forget_password_token_expiration = expiration_time
            user_profile.save()

            send_password_reset_email(contact_info, token)

            messages.success(request, "ایمیل تغییر رمز عبور برای شما ارسال شد. لطفاً ایمیل خود را بررسی کنید.")
            return redirect("forgot-password")

        # Mobile case
        elif contact_info.isdigit() and len(contact_info) == 11:  # Assuming 11-digit mobile numbers
            user = User.objects.filter(profile__mobile=contact_info).first()
            if not user:
                messages.error(request, "کاربری با این شماره موبایل وجود ندارد.")
                return redirect("forgot-password")

            # Use external SMS service to send OTP
            otp = send_otp(contact_info)  # Assume this returns a success/fail status
            expiration_time = timezone.now() + timezone.timedelta(minutes=10)
            # Store OTP and expiration in session
            request.session['encrypted_otp'] = encrypt_otp(otp)
            request.session['otp_expiration_time'] = expiration_time.isoformat()
            request.session['mobile'] = encrypt_otp(contact_info)
            messages.success(request, "کد تایید به موبایل شما ارسال شد.")
            return redirect("verify_otp_rest_password")  # Redirect to OTP verification page

        else:
            messages.error(request, "لطفاً ایمیل یا شماره موبایل معتبر وارد کنید.")
            return redirect("forgot-password")
