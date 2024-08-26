from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from auth.views import AuthView


class LoginView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("index")  # Replace 'index' with the actual URL name for the home page

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            username_or_email_or_mobile = request.POST.get("email-username-mobile")
            password = request.POST.get("password")

            if not (username_or_email_or_mobile and password):
                messages.error(request, "لطفا نام کاربری و رمز ورود را وارد کنید.")
                return redirect("login")

            # Check if the input is an email
            if "@" in username_or_email_or_mobile:
                user = User.objects.filter(email=username_or_email_or_mobile).first()
                if user is None:
                    messages.error(request, "ایمیلی معتبر وارد کنید.")
                    return redirect("login")
                username_or_email_or_mobile = user.username

            # Check if the input is a mobile number
            elif username_or_email_or_mobile.isdigit() and len(username_or_email_or_mobile) == 11:  # Assuming mobile numbers are 11 digits
                user = User.objects.filter(profile__mobile=username_or_email_or_mobile).first()  # Assuming you have a Profile model with a mobile field
                if user is None:
                    messages.error(request, "شماره موبایل معتبر وارد کنید.")
                    return redirect("login")
                username_or_email_or_mobile = user.username

            else:
                user = User.objects.filter(username=username_or_email_or_mobile).first()
                if user is None:
                    messages.error(request, "نام کاربری معتبر وارد کنید.")
                    return redirect("login")

            # Authenticate the user
            authenticated_user = authenticate(request, username=username_or_email_or_mobile, password=password)
            if authenticated_user is not None:
                # Login the user if authentication is successful
                login(request, authenticated_user)

                # Redirect to the page the user was trying to access before logging in
                if "next" in request.POST:
                    return redirect(request.POST["next"])
                else:
                    # Redirect to the home page or another appropriate page
                    return redirect("index")
            else:
                messages.error(request, "نام کاربری یا رمز عبور نادرست است.")
                return redirect("login")
