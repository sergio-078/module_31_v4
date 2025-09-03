from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
import secrets
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, choices=[('ru', 'Russian'), ('en', 'English')], default='ru')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

class EmailVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_verification(cls, user):
        cls.objects.filter(user=user).delete()
        code = secrets.token_urlsafe(32)
        verification = cls.objects.create(user=user, code=code)
        return verification

    def is_valid(self):
        return (timezone.now() - self.created_at) < timedelta(hours=24)

    def get_expiration_time(self):
        return self.created_at + timedelta(hours=24)

    def send_verification_email(self):
        subject = _('Email Verification - MMORPG Portal')
        verification_url = f"{settings.SITE_URL}/user/verify/{self.code}/"
        expiration_time = self.get_expiration_time()

        message = _(
            'Welcome to MMORPG Portal!\n\n'
            'Please verify your email by clicking the following link:\n'
            '{}\n\n'
            'This verification link is valid for 24 hours until {} (UTC).\n'
            'If you do not verify your email within 24 hours, '
            'you will need to register again.\n\n'
            'Best regards,\n'
            'MMORPG Portal Team'
        ).format(verification_url, expiration_time.strftime("%Y-%m-%d %H:%M:%S"))

        # Для разработки
        print(f"\n=== EMAIL VERIFICATION ===")
        print(f"To: {self.user.email}")
        print(f"Subject: {subject}")
        print(f"Link: {verification_url}")
        print(f"Expires: {expiration_time}")
        print("=======================\n")

        # Отправляем письмо
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            fail_silently=False,
        )

class UserActionLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('User Action Log')
        verbose_name_plural = _('User Action Logs')

    def __str__(self):
        return f"{self.user.email if self.user else 'Anonymous'} - {self.action}"
