from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import pytz

from .forms import RegistrationForm, ProfileForm
from .models import CustomUser, EmailVerification, UserActionLog


class CustomLogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        # Обрабатываем GET запросы как POST для удобства
        return self.post(request, *args, **kwargs)


class RegisterView(View):
    template_name = 'appUser/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            verification = EmailVerification.create_verification(user)
            verification.send_verification_email()

            messages.success(request, _(
                'Registration successful! '
                'Please check your email for verification link. '
                'Link is valid for 24 hours.'
            ))

            UserActionLog.objects.create(
                user=user,
                action="Registered new account",
                ip_address=getattr(request, 'user_ip', None)
            )
            return redirect('login')

        return render(request, self.template_name, {'form': form})


def verify_email(request, code):
    try:
        verification = EmailVerification.objects.get(code=code)

        if not verification.is_valid():
            messages.error(request, _('Verification link has expired. Please register again.'))
            verification.delete()
            return redirect('register')

        user = verification.user
        user.is_active = True
        user.save()
        verification.delete()

        messages.success(request, _('Email verified successfully! You can now log in.'))
        UserActionLog.objects.create(
            user=user,
            action="Email verified successfully",
            ip_address=getattr(request, 'user_ip', None)
        )
        return redirect('login')

    except EmailVerification.DoesNotExist:
        messages.error(request, _('Invalid verification link.'))
        return redirect('register')


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully!'))
            UserActionLog.objects.create(
                user=user,
                action="Updated profile",
                ip_address=getattr(request, 'user_ip', None)
            )
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'appUser/profile.html', {
        'form': form,
        'timezones': pytz.all_timezones
    })


@login_required
def set_timezone(request):
    if request.method == 'POST':
        timezone = request.POST.get('timezone')
        if timezone in pytz.all_timezones:
            request.session['django_timezone'] = timezone
            request.user.timezone = timezone
            request.user.save()
            messages.success(request, _('Timezone updated successfully!'))
            UserActionLog.objects.create(
                user=request.user,
                action=f"Changed timezone to {timezone}",
                ip_address=getattr(request, 'user_ip', None)
            )
        else:
            messages.error(request, _('Invalid timezone.'))
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in [lang[0] for lang in settings.LANGUAGES]:
            request.session['django_language'] = language
            request.user.language = language
            request.user.save()
            messages.success(request, _('Language changed successfully!'))
            UserActionLog.objects.create(
                user=request.user,
                action=f"Changed language to {language}",
                ip_address=getattr(request, 'user_ip', None)
            )
        else:
            messages.error(request, _('Invalid language.'))
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def custom_password_reset(request):
    if request.method == 'POST':
        try:
            response = auth_views.PasswordResetView.as_view(
                template_name='appUser/password_reset.html',
                email_template_name='appUser/password_reset_email.html',
                subject_template_name='appUser/password_reset_subject.txt',
                success_url='/user/password_reset/done/'
            )(request)
            return response
        except Exception as e:
            messages.error(request, _('Could not send email. Please contact administrator.'))
            return redirect('password_reset')

    return auth_views.PasswordResetView.as_view(
        template_name='appUser/password_reset.html',
        email_template_name='appUser/password_reset_email.html',
        subject_template_name='appUser/password_reset_subject.txt',
        success_url='/user/password_reset/done/'
    )(request)
