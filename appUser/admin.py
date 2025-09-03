from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerification, UserActionLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'timezone', 'language')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'code']


@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['timestamp']
    search_fields = ['user__email', 'action']
