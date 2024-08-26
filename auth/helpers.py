from cryptography.fernet import Fernet
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
import requests
from django.utils import timezone
from utils.melipayamak import Api

# Replace with your Melipayamak credentials
MELIPAYAMAK_USERNAME = "09177157497"
MELIPAYAMAK_PASSWORD = "Fyg?S9RRyP!"
SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with your actual secret key
FERNET_KEY = "Z8cuHnX0RhjFEmWCs--l9l6KydOqR9kHywkOhY_TvXg="  # Example using Django's SECRET_KEY for simplicity

# Initialize the Melipayamak API
api = Api(MELIPAYAMAK_USERNAME, MELIPAYAMAK_PASSWORD)
sms = api.sms()


def send_email(subject, email, message):
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.send()
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_absolute_url(path):
    return settings.BASE_URL + path


def send_verification_email(email, token):
    subject = "تایید ایمیل"
    verification_url = get_absolute_url(reverse('verify-email', kwargs={'token': token}))
    message = f"سلام,\n\nلطفا با کلیک بر روی لینک زیر ایمیل را تایید کنید: {verification_url}"
    send_email(subject, email, message)


def send_password_reset_email(email, token):
    subject = "ریست کردن رمزورود"
    reset_url = get_absolute_url(reverse('reset-password', kwargs={'token': token}))
    message = f"سلام,\n\nلطفا با استفاده از لینک زیر رمز خود را تغییر دهید: {reset_url}"
    send_email(subject, email, message)


def send_otp(mobile):
    # Define the API endpoint and data payload
    url = "https://console.melipayamak.com/api/send/otp/d317efb1acf147ad943589d517ae4c22"
    data = { 'to': mobile }

    try:
        # Send the OTP request
        response = requests.post(url, json=data)
        response_data = response.json()

        # Check if the request was successful
        if response_data['status'] == 'ارسال موفق بود':
            otp = response_data['code']
            print(f"OTP sent to {mobile}: {otp}")
            return otp
        else:
            print(f"Failed to send OTP: {response_data['status']}")
            return None
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return None


def verify_otp_from_session(request, otp_input):
    """Verify the OTP by decrypting it from the session and comparing it with the input."""
    encrypted_otp = request.session.get('encrypted_otp')
    mobile = request.session.get('mobile')
    otp_expiration_time = request.session.get('otp_expiration_time')
    print(encrypted_otp)
    print(mobile)
    print(otp_expiration_time)
    if not encrypted_otp or not mobile or not otp_expiration_time:
        print("No OTP, mobile number, or expiration time found in session.")
        return False

    # Convert expiration time back to a datetime object
    expiration_time = timezone.datetime.fromisoformat(otp_expiration_time)

    # Check if the OTP has expired
    if timezone.now() > expiration_time:
        print("OTP has expired.")
        return False

    decrypted_otp = decrypt_otp(encrypted_otp)
    print(f"Decrypted OTP from Session: {decrypted_otp}")

    if decrypted_otp == otp_input:
        print("OTP verified successfully.")
        return True
    else:
        print("OTP verification failed.")
        return False


def encrypt_otp(otp):
    """Encrypt the OTP using Fernet symmetric encryption."""
    fernet = Fernet(FERNET_KEY)
    return fernet.encrypt(otp.encode()).decode()


def decrypt_otp(encrypted_otp):
    """Decrypt the OTP using Fernet symmetric encryption."""
    fernet = Fernet(FERNET_KEY)
    return fernet.decrypt(encrypted_otp.encode()).decode()
