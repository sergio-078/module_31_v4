from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(
        template_name='appUser/login.html',
        extra_context={'title': _('Login')}
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        template_name='appUser/logout.html',
        next_page='/'
    ), name='logout'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/<str:code>/', views.verify_email, name='verify_email'),
    path('verification/sent/', views.verification_sent, name='verification_sent'),
    path('verification/', views.VerificationView.as_view(), name='verification'),

    # Password reset
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='appUser/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='appUser/password_reset_confirm.html',
             success_url='/user/reset/done/'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='appUser/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Timezone/Language
    path('set-timezone/', views.set_timezone, name='set_timezone'),
    path('set-language/', views.set_language, name='set_language'),
]
