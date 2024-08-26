from cryptography.fernet import Fernet
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

from config import settings

# Generate a key for encryption/decryption
# Normally, you would do this once and store the key securely

cipher_suite = Fernet(settings.FERNET_KEY.encode())  # Assuming SECRET_KEY is 32+ bytes long

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)   # Use unique=True for unique email addresses
    email_token = models.CharField(max_length=100, blank=True, null=True)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, email=instance.email)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Otp(models.Model):
    mobile = models.CharField(max_length=15)
    encrypted_otp = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.invalidate_previous_otps()
        super().save(*args, **kwargs)

    def invalidate_previous_otps(self):
        Otp.objects.filter(mobile=self.mobile, is_used=False, expires_at__gt=timezone.now()).update(is_used=True)

    def decrypt_otp(self):
        cipher_suite = Fernet(settings.FERNET_KEY.encode())
        return cipher_suite.decrypt(self.encrypted_otp.encode()).decode()

    @classmethod
    def verify_otp(cls, mobile, otp_input):
        try:
            otp_record = cls.objects.filter(mobile=mobile, is_used=False, expires_at__gt=timezone.now()).latest('created_at')
            decrypted_otp = otp_record.decrypt_otp()
            if decrypted_otp == otp_input:
                otp_record.is_used = True
                otp_record.save()
                return True
        except cls.DoesNotExist:
            pass
        return False
