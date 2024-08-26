from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from auth.views import AuthView
from auth.models import Profile
from auth.helpers import send_verification_email, send_otp, verify_otp_from_session
import uuid


class VerifyMobileView(AuthView):
    def post(self, request):
        otp_input = request.POST.get('otp')
        mobile = request.session.get('mobile')

        if mobile and otp_input:
            if verify_otp_from_session(request, otp_input):
                messages.success(request, "OTP verified successfully!")
                profile = Profile.objects.filter(mobile=mobile).filter()
                profile.is_verified = True
                profile.save()
                # Optionally, mark the user as verified here
                return redirect('login')  # Redirect to login or dashboard
            else:
                messages.error(request, "Invalid OTP or OTP has expired.")
        else:
            messages.error(request, "Please enter the OTP.")

        return redirect('verify-otp')


class ResendOTPView(AuthView):
    def get(self, request):
        mobile = request.session.get('mobile')
        if mobile:
            send_otp(mobile)  # Resend the OTP
            messages.success(request, f"OTP has been resent to {mobile}")
        else:
            messages.error(request, "Unable to resend OTP. Please try registering again.")

        return redirect('verify-otp')


class VerifyOtpView(AuthView):
    def get(self, request):
        # Render the login page for users who are not logged in.
        mobile = request.session.get('mobile')
        return super().get(request, mobile)


class SendVerificationOtpView(AuthView):
    def get(self, request):
        email, message = self.get_email_and_message(request)

        if email:
            token = str(uuid.uuid4())
            user_profile = Profile.objects.filter(email=email).first()
            user_profile.email_token = token
            user_profile.save()
            send_verification_email(email, token)
            messages.success(request, message)
        else:
            messages.error(request, "ایمیل یافت نشد")

        return redirect("verify-email-page")

    def get_otp_and_message(self, request):
        if request.user.is_authenticated:
            email = request.user.profile.email

            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                message = messages.success(request, "ایمیل تایید با موفقیت ارسال شد")
            else:
                message = messages.error(request,
                                         "تنظیمات ایمیل به درستی تنظیم نشده است و امکان ارسال ایمیل وجود ندارد.")

        else:
            email = request.session.get('email')
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                message = "ایمیل مجدد با موفقیت ارسال شد" if email else None
            else:
                message = messages.error(request,
                                         "تنظیمات ایمیل به درستی تنظیم نشده است و امکان ارسال ایمیل وجود ندارد.")

        return email, message
